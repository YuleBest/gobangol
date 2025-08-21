import asyncio
import json
import logging
from datetime import datetime, timedelta
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import aiosqlite
import uuid
import random
import string
import re
from contextlib import asynccontextmanager

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("room-server")

rooms_cache = {}  # roomId -> {players, spectators, messages, sockets, joinTokens, lastActivityTime}
ROOM_TIMEOUT_SECONDS = 120  # 2分钟无活动自动销毁房间

async def init_db():
    async with aiosqlite.connect("db.sqlite") as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id TEXT PRIMARY KEY,
            creator TEXT,
            players TEXT,
            spectators TEXT,
            password TEXT,
            roomStatus TEXT,
            createdAt INTEGER
        )
        """)
        await db.commit()
        logger.info("数据库初始化完成")

async def check_room_timeout():
    """定期检查房间超时并销毁无活动房间"""
    while True:
        try:
            await asyncio.sleep(10)  # 每10秒检查一次
            current_time = datetime.utcnow().timestamp()
            rooms_to_delete = []
            
            for room_id, room in rooms_cache.items():
                last_activity = room.get("lastActivityTime", room.get("createdAt", 0))
                if current_time - last_activity > ROOM_TIMEOUT_SECONDS:
                    rooms_to_delete.append(room_id)
            
            for room_id in rooms_to_delete:
                room = rooms_cache.get(room_id)
                if room:
                    logger.info("[TIMER] 房间 %s 超时无活动，自动销毁", room_id)
                    # 通知所有用户房间即将关闭
                    for s in room["sockets"]:
                        try:
                            await s.send_text(json.dumps({"action": "roomTimeout", "payload": {"message": "房间因长时间无活动已关闭"}}))
                            await s.send_text(json.dumps({"action": "roomClosed"}))
                        except:
                            pass
                    # 删除房间
                    del rooms_cache[room_id]
                    logger.info("[TIMER] 房间 %s 已销毁", room_id)
                    
        except Exception as e:
            logger.error("[TIMER] 检查房间超时时发生错误: %s", str(e))

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    # 启动后台定时任务
    timeout_task = asyncio.create_task(check_room_timeout())
    logger.info("服务启动完成")
    yield
    # 清理后台任务
    timeout_task.cancel()
    try:
        await timeout_task
    except asyncio.CancelledError:
        pass
    logger.info("服务已关闭")

app = FastAPI(lifespan=lifespan)

def validate_nickname(nickname):
    if not nickname:
        return False
    pattern = re.compile(r'[/<>\[\]*^@#]')
    if pattern.search(nickname):
        return False
    return True

def room_for_frontend(room, admin=False):
    room_copy = room.copy()
    room_copy.pop("sockets", None)
    room_copy.pop("joinTokens", None)
    if not admin and room_copy.get("password"):
        room_copy["password"] = "***"
    return room_copy

def generate_token(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def cleanup_expired_tokens(room, expire_seconds=60):
    now = datetime.utcnow().timestamp()
    tokens_to_delete = [t for t, info in room.get("joinTokens", {}).items()
                        if info["used"] or now - info["createdAt"] > expire_seconds]
    for t in tokens_to_delete:
        del room["joinTokens"][t]

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    client_id = str(uuid.uuid4())
    logger.info("[WS] 客户端连接: %s", client_id)

    user_room = None
    current_user = None

    try:
        while True:
            data = await ws.receive_text()
            msg = json.loads(data)
            action = msg.get("action")
            payload = msg.get("payload", {})
            logger.debug("[WS] 收到消息: %s", msg)
            
            # 记录用户信息用于断开连接处理
            if action in ["createRoom", "joinRoom"]:
                current_user = payload.get("creator") or payload.get("user")

            # ---------------- 创建房间 ----------------
            if action == "createRoom":
                roomId = payload.get("roomId")
                if not roomId:
                    while True:
                        new_id = ''.join(random.choices(string.digits, k=6))
                        if new_id not in rooms_cache:
                            roomId = new_id
                            break
                creator_name = payload.get("creator")
                if not validate_nickname(creator_name):
                    await ws.send_text(json.dumps({"action": "error", "payload": "昵称不能包含特殊字符"}))
                    continue
                password = payload.get("password", "")
                now = int(datetime.utcnow().timestamp())
                room = {
                    "id": roomId,
                    "creator": creator_name,
                    "players": [creator_name],
                    "spectators": [],
                    "password": password,
                    "roomStatus": "waiting",
                    "createdAt": now,
                    "messages": [],
                    "sockets": set([ws]),
                    "joinTokens": {},
                    "lastActivityTime": datetime.utcnow().timestamp()
                }
                # 生成 joinToken
                token = generate_token()
                room["joinTokens"][token] = {"user": creator_name, "used": False, "createdAt": datetime.utcnow().timestamp()}
                rooms_cache[roomId] = room
                user_room = roomId
                room["lastActivityTime"] = datetime.utcnow().timestamp()
                await ws.send_text(json.dumps({"action": "roomCreated", "payload": {"id": roomId, "joinToken": token, **room_for_frontend(room)}}))
                logger.info("[WS] 创建房间: %s by %s", roomId, creator_name)

            # ---------------- 请求临时 token ----------------
            elif action == "requestToken":
                roomId = payload.get("roomId")
                user = payload.get("user")
                room = rooms_cache.get(roomId)
                if not room:
                    await ws.send_text(json.dumps({"action": "error", "payload": "房间不存在"}))
                    continue
                if user in room["players"] or user in room["spectators"]:
                    await ws.send_text(json.dumps({"action": "error", "payload": "你已在房间中"}))
                    continue
                cleanup_expired_tokens(room)
                token = generate_token()
                room["joinTokens"][token] = {"user": user, "used": False, "createdAt": datetime.utcnow().timestamp()}
                await ws.send_text(json.dumps({"action": "roomCreated", "payload": {"id": roomId, "joinToken": token}}))

            # ---------------- 加入房间 ----------------
            elif action == "joinRoom":
                roomId = payload.get("roomId")
                user = payload.get("user")
                password = payload.get("password", "")
                token = payload.get("joinToken", "")
                room = rooms_cache.get(roomId)
                if not room:
                    await ws.send_text(json.dumps({"action": "error", "payload": "房间不存在"}))
                    continue
                if room["password"] and room["password"] != password:
                    await ws.send_text(json.dumps({"action": "error", "payload": "密码错误"}))
                    continue
                cleanup_expired_tokens(room)
                token_info = room.get("joinTokens", {}).get(token)
                if not token_info or token_info["used"] or token_info["user"] != user:
                    await ws.send_text(json.dumps({"action": "error", "payload": "token无效或已使用"}))
                    continue
                token_info["used"] = True  # 标记已使用
                if user not in room["players"] and user not in room["spectators"]:
                    if len(room["players"]) < 2:
                        room["players"].append(user)
                        if len(room["players"]) == 2:
                            room["roomStatus"] = "spectating"
                    elif len(room["players"]) + len(room["spectators"]) < 12:
                        room["spectators"].append(user)
                        room["roomStatus"] = "spectating"
                    else:
                        await ws.send_text(json.dumps({"action": "error", "payload": "房间已满"}))
                        continue
                room["sockets"].add(ws)
                user_room = roomId
                room["lastActivityTime"] = datetime.utcnow().timestamp()  # 更新最后活动时间
                await ws.send_text(json.dumps({"action": "joinedRoom", "payload": room_for_frontend(room)}))
                update = {"players": room["players"], "spectators": room["spectators"], "roomStatus": room["roomStatus"]}
                for s in room["sockets"]:
                    if s != ws:
                        await s.send_text(json.dumps({"action": "roomUpdate", "payload": update}))
                logger.info("[WS] 用户 %s 加入房间 %s", user, roomId)

            # ---------------- 离开房间 ----------------
            elif action == "leaveRoom":
                roomId = payload.get("roomId")
                user = payload.get("user")
                room = rooms_cache.get(roomId)
                if room:
                    room["players"] = [p for p in room["players"] if p != user]
                    room["spectators"] = [s for s in room["spectators"] if s != user]
                    room["sockets"].discard(ws)
                    update = {"players": room["players"], "spectators": room["spectators"], "roomStatus": room["roomStatus"]}
                    for s in room["sockets"]:
                        await s.send_text(json.dumps({"action": "roomUpdate", "payload": update}))
                    if not room["players"] and not room["spectators"]:
                        for s in room["sockets"]:
                            await s.send_text(json.dumps({"action": "roomClosed"}))
                        del rooms_cache[roomId]

            # ---------------- 消息 ----------------
            elif action == "sendMessage":
                roomId = payload.get("roomId")
                room = rooms_cache.get(roomId)
                if room:
                    room["messages"].append(payload)
                    room["lastActivityTime"] = datetime.utcnow().timestamp()  # 更新最后活动时间
                    for s in room["sockets"]:
                        await s.send_text(json.dumps({"action": "newMessage", "payload": payload}))

            # ---------------- 房间列表 ----------------
            elif action == "getRoomList":
                list_payload = [room_for_frontend(r) for r in rooms_cache.values()]
                await ws.send_text(json.dumps({"action": "roomList", "payload": list_payload}))

            # ---------------- 销毁房间 ----------------
            elif action == "destroyRoom":
                roomId = payload.get("roomId")
                room = rooms_cache.get(roomId)
                if room:
                    for s in room["sockets"]:
                        await s.send_text(json.dumps({"action": "roomClosed"}))
                    del rooms_cache[roomId]

    except WebSocketDisconnect:
        logger.info("[WS] 客户端断开连接: %s, 用户: %s", client_id, current_user)
        if user_room and current_user:
            room = rooms_cache.get(user_room)
            if room:
                room["sockets"].discard(ws)
                
                # 将断开连接的用户从房间中移除
                original_players_count = len(room["players"])
                original_spectators_count = len(room["spectators"])
                
                room["players"] = [p for p in room["players"] if p != current_user]
                room["spectators"] = [s for s in room["spectators"] if s != current_user]
                
                # 更新房间状态
                if len(room["players"]) < 2:
                    room["roomStatus"] = "waiting"
                
                # 检查房间是否为空
                if not room["players"] and not room["spectators"]:
                    # 房间为空，删除房间
                    for s in room["sockets"]:
                        try:
                            await s.send_text(json.dumps({"action": "roomClosed"}))
                        except:
                            pass
                    del rooms_cache[user_room]
                    logger.info("[WS] 房间 %s 已关闭（所有用户离开）", user_room)
                else:
                    # 通知其他用户房间更新
                    update = {
                        "players": room["players"], 
                        "spectators": room["spectators"], 
                        "roomStatus": room["roomStatus"],
                        "disconnectedUser": current_user
                    }
                    for s in room["sockets"]:
                        try:
                            await s.send_text(json.dumps({"action": "roomUpdate", "payload": update}))
                            await s.send_text(json.dumps({"action": "userLeft", "payload": {"user": current_user, "message": f"用户 {current_user} 已离开房间"}}))
                        except:
                            pass
                    logger.info("[WS] 用户 %s 已从房间 %s 中移除", current_user, user_room)
        elif user_room:
            # 只有房间信息但没有用户信息，只移除socket
            room = rooms_cache.get(user_room)
            if room:
                room["sockets"].discard(ws)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=3000, reload=True)