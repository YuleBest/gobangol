import asyncio
import json
import logging
from datetime import datetime, timedelta
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import aiosqlite
import uuid
import random
import string
import re
from contextlib import asynccontextmanager

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("room-server")

rooms_cache = {}  # roomId -> {players, spectators, messages, sockets, joinTokens, lastActivityTime}
token_cache = {}  # token -> {roomId, user, type, used, createdAt}  type: 'creator' or 'joiner'
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

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境应该配置具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

def create_token(room_id, user, token_type):
    """创建一次性Token"""
    token = generate_token()
    token_cache[token] = {
        "roomId": room_id,
        "user": user,
        "type": token_type,  # 'creator' or 'joiner'
        "used": False,
        "createdAt": datetime.utcnow().timestamp()
    }
    return token

def validate_token(token):
    """验证Token有效性，使用后立即失效"""
    token_info = token_cache.get(token)
    if not token_info or token_info["used"]:
        return None
    
    # 检查房间是否存在
    room = rooms_cache.get(token_info["roomId"])
    if not room:
        return None
    
    return token_info

def get_room_info_by_token(token):
    """通过Token获取房间信息"""
    token_info = token_cache.get(token)
    if not token_info or token_info["used"]:
        return None
    
    room = rooms_cache.get(token_info["roomId"])
    if not room:
        return None
    
    return {
        "roomId": room["id"],
        "creator": room["creator"],
        "user": token_info["user"],  # 当前用户的昵称
        "userType": token_info["type"],  # 'creator' or 'joiner'
        "players": room["players"],
        "spectators": room["spectators"],
        "roomStatus": room["roomStatus"],
        "messages": room["messages"]
    }

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
                # 生成创建者Token
                token = create_token(roomId, creator_name, "creator")
                rooms_cache[roomId] = room
                user_room = roomId
                room["lastActivityTime"] = datetime.utcnow().timestamp()
                await ws.send_text(json.dumps({"action": "roomCreated", "payload": {"token": token}}))
                logger.info("[WS] 创建房间: %s by %s", roomId, creator_name)

            # ---------------- 请求加入房间Token ----------------
            elif action == "requestJoinToken":
                roomId = payload.get("roomId")
                user = payload.get("user")
                room = rooms_cache.get(roomId)
                if not room:
                    await ws.send_text(json.dumps({"action": "error", "payload": "房间不存在"}))
                    continue
                if user in room["players"] or user in room["spectators"]:
                    await ws.send_text(json.dumps({"action": "error", "payload": "你已在房间中"}))
                    continue
                
                # 检查房间密码
                password = payload.get("password", "")
                if room["password"] and room["password"] != password:
                    await ws.send_text(json.dumps({"action": "error", "payload": "密码错误"}))
                    continue
                
                # 生成加入者Token
                token = create_token(roomId, user, "joiner")
                await ws.send_text(json.dumps({"action": "joinToken", "payload": {"token": token}}))

            # ---------------- 通过Token加入房间 ----------------
            elif action == "joinRoom":
                token = payload.get("token", "")
                if not token:
                    await ws.send_text(json.dumps({"action": "error", "payload": "缺少Token"}))
                    continue
                
                # 验证Token
                token_info = validate_token(token)
                if not token_info:
                    await ws.send_text(json.dumps({"action": "error", "payload": "Token无效或已使用"}))
                    continue
                
                # 标记Token为已使用（真正使用时才标记）
                token_cache[token]["used"] = True
                
                roomId = token_info["roomId"]
                user = token_info["user"]
                room = rooms_cache.get(roomId)
                if not room:
                    await ws.send_text(json.dumps({"action": "error", "payload": "房间不存在"}))
                    continue
                
                # 添加用户到房间
                if user not in room["players"] and user not in room["spectators"]:
                    if len(room["players"]) < 2:
                        room["players"].append(user)
                        if len(room["players"]) == 2:
                            room["roomStatus"] = "playing"
                    elif len(room["players"]) + len(room["spectators"]) < 12:
                        room["spectators"].append(user)
                        room["roomStatus"] = "playing"
                    else:
                        await ws.send_text(json.dumps({"action": "error", "payload": "房间已满"}))
                        continue
                
                room["sockets"].add(ws)
                user_room = roomId
                current_user = user  # 设置当前用户
                room["lastActivityTime"] = datetime.utcnow().timestamp()
                
                # 发送包含历史消息的完整房间信息
                room_data = room_for_frontend(room)
                room_data["messages"] = room["messages"]
                await ws.send_text(json.dumps({"action": "joinedRoom", "payload": room_data}))
                
                # 通知其他用户房间更新
                update = {"players": room["players"], "spectators": room["spectators"], "roomStatus": room["roomStatus"]}
                for s in room["sockets"]:
                    if s != ws:
                        await s.send_text(json.dumps({"action": "roomUpdate", "payload": update}))
                        await s.send_text(json.dumps({"action": "userJoined", "payload": {"user": user, "message": f"用户 {user} 加入了房间"}}))
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
                    # 确保消息包含用户名
                    player_name = payload.get("playerName", current_user or "未知用户")
                    message_data = {
                        "playerName": player_name,
                        "message": payload.get("message", ""),
                        "roomId": roomId,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    room["messages"].append(message_data)
                    room["lastActivityTime"] = datetime.utcnow().timestamp()  # 更新最后活动时间
                    
                    # 向房间内所有用户广播消息
                    disconnected_sockets = set()
                    for s in room["sockets"]:
                        try:
                            await s.send_text(json.dumps({"action": "newMessage", "payload": message_data}))
                            logger.debug("[WS] 消息已发送给用户: %s", id(s))
                        except Exception as e:
                            logger.error("[WS] 发送消息失败: %s", str(e))
                            disconnected_sockets.add(s)
                    
                    # 清理断开的连接
                    for s in disconnected_sockets:
                        room["sockets"].discard(s)

            # ---------------- 房间列表 ----------------
            elif action == "getRoomList":
                list_payload = [room_for_frontend(r) for r in rooms_cache.values()]
                await ws.send_text(json.dumps({"action": "roomList", "payload": list_payload}))

            # ---------------- 获取房间信息 ----------------
            elif action == "getRoomInfo":
                roomId = payload.get("roomId")
                room = rooms_cache.get(roomId)
                if room and roomId in rooms_cache:
                    room_data = room_for_frontend(room)
                    room_data["messages"] = room["messages"]
                    await ws.send_text(json.dumps({"action": "roomInfo", "payload": room_data}))
                else:
                    await ws.send_text(json.dumps({"action": "error", "payload": "房间不存在"}))

            # ---------------- 通过Token获取房间信息 ----------------
            elif action == "getRoomByToken":
                token = payload.get("token", "")
                if not token:
                    await ws.send_text(json.dumps({"action": "error", "payload": "缺少Token"}))
                    continue
                
                room_info = get_room_info_by_token(token)
                if not room_info:
                    await ws.send_text(json.dumps({"action": "error", "payload": "Token无效或已使用"}))
                    continue
                
                await ws.send_text(json.dumps({"action": "roomInfo", "payload": room_info}))

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

@app.get("/getRoomByToken")
async def get_room_by_token(token: str):
    """通过Token获取房间信息的HTTP接口"""
    room_info = get_room_info_by_token(token)
    if not room_info:
        return JSONResponse(
            status_code=404,
            content={"error": "Token无效或已使用"}
        )
    return JSONResponse(content=room_info)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)