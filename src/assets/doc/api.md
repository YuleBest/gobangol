# 在线房间系统 API 文档

## 基础信息

- **协议**：WebSocket
- **URL**：`ws://<服务器 IP>:3000/ws`
- **消息格式**：JSON

**字段说明**：

- `action`：操作类型
- `payload`：操作数据

---

## 客户端事件（发送到服务器）

### 1. 创建房间

#### 请求

```json
{
  "action": "createRoom",
  "payload": {
    "creator": "玩家昵称",
    "password": "房间密码（可选）"
  }
}
```

#### 响应

```json
{
  "action": "roomCreated",
  "payload": {
    "id": "房间 ID",
    "creator": "玩家昵称",
    "players": ["玩家昵称"],
    "spectators": [],
    "password": "房间密码",
    "roomStatus": "waiting",
    "createdAt": 1680000000,
    "messages": []
  }
}
```

---

### 2. 获取房间列表

#### 请求

```json
{
  "action": "getRoomList"
}
```

#### 响应

```json
{
  "action": "roomList",
  "payload": [
    {
      "id": "房间 ID",
      "creator": "玩家昵称",
      "players": ["玩家 1", "玩家 2"],
      "spectators": ["观众 1"],
      "roomStatus": "waiting"
    }
  ]
}
```

> 仅返回无密码房间。

---

### 3. 加入房间

#### 请求

```json
{
  "action": "joinRoom",
  "payload": {
    "roomId": "房间 ID",
    "user": "玩家昵称",
    "password": "房间密码（如果有）"
  }
}
```

#### 响应

##### 成功

```json
{
  "action": "joinedRoom",
  "payload": {
    "id": "房间 ID",
    "creator": "玩家昵称",
    "players": ["玩家 1", "玩家 2"],
    "spectators": ["观众 1"],
    "roomStatus": "spectating",
    "messages": []
  }
}
```

##### 失败

```json
{
  "action": "error",
  "payload": "房间不存在或密码错误"
}
```

---

### 4. 离开房间

#### 请求

```json
{
  "action": "leaveRoom",
  "payload": {
    "roomId": "房间 ID",
    "user": "玩家昵称"
  }
}
```

#### 广播

其他房间成员收到更新：

```json
{
  "action": "roomUpdate",
  "payload": {
    "players": ["玩家 1"],
    "spectators": ["观众 1"],
    "roomStatus": "waiting"
  }
}
```

##### 如果房间空了：

```json
{
  "action": "roomClosed"
}
```

---

### 5. 销毁房间（房主操作）

#### 请求

```json
{
  "action": "destroyRoom",
  "payload": {
    "roomId": "房间 ID"
  }
}
```

#### 广播

```json
{
  "action": "roomClosed"
}
```

---

### 6. 发送聊天消息

#### 请求

```json
{
  "action": "sendMessage",
  "payload": {
    "roomId": "房间 ID",
    "playerName": "发送者昵称",
    "message": "消息内容"
  }
}
```

#### 广播

```json
{
  "action": "newMessage",
  "payload": {
    "playerName": "发送者昵称",
    "message": "消息内容"
  }
}
```

---

### 7. 房间状态更新（服务器广播）

#### 触发条件

- 玩家加入、离开房间
- 房间被销毁或状态变化

#### 消息示例

```json
{
  "action": "roomUpdate",
  "payload": {
    "players": ["玩家 1", "玩家 2"],
    "spectators": ["观众 1"],
    "roomStatus": "spectating"
  }
}
```

---

### 8. 错误消息

#### 通用错误消息

```json
{
  "action": "error",
  "payload": "错误描述文本"
}
```

---

## 附加说明

1. 每个房间最大玩家数：2
2. 每个房间最大观众数：10（总人数不超过 12）
3. 密码房间不会显示在 `roomList` 中，但持有房间 ID 和密码的人可以加入。
4. `roomStatus` 可为：
   - `"waiting"`：等待玩家
   - `"spectating"`：观战中
