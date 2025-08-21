<template>
  <div class="main">
    <div class="title">
      <div class="leave-and-info">
        <div class="leave">
          <button @click="leaveRoom">
            <v-icon>mdi-arrow-left</v-icon>
          </button>
        </div>
        <div class="roomInfo">
          <h2>五子棋房间</h2>
          <p>{{ roomStatusText }}</p>
        </div>
      </div>

      <div class="roomId">
        <button @click="copyRoomId">
          <v-icon>mdi-content-copy</v-icon>
        </button>
        <code>{{ roomId }}</code>
      </div>
    </div>

    <!-- 聊天区域 -->
    <div class="chat">
      <v-divider thickness="1"></v-divider>

      <div class="chat-messages" ref="chatContainer">
        <div
          v-if="messages.length === 0"
          class="no-messages text-center grey--text"
        >
          暂无消息
        </div>
        <div
          v-for="(msg, idx) in messages"
          :key="idx"
          class="message-wrapper"
          :class="{ 'my-message': msg.playerName === creator }"
        >
          <div class="message-bubble">
            <div class="message-content">
              <div class="message-header">
                <span class="message-sender font-weight-bold">
                  {{ msg.playerName }}
                </span>
                <span class="message-time text-caption">
                  {{ formatTime(msg.timestamp || new Date()) }}
                </span>
              </div>
              <div
                class="message-text"
                :class="{
                  'my-message-text': msg.playerName === creator,
                  'others-message-text': msg.playerName !== creator,
                }"
              >
                {{ msg.message }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <v-divider thickness="1"></v-divider>
    </div>

    <!-- 输入区域 -->
    <div class="chat-input">
      <v-icon>mdi-message</v-icon>
      <v-text-field
        label="发送消息..."
        variant="outlined"
        hide-details="auto"
        @keyup.enter="sendMessage"
        v-model="chatInput"
      ></v-text-field>
      <button @click="sendMessage" :disabled="!chatInput.trim()">
        <v-icon>mdi-send</v-icon>
      </button>
    </div>
  </div>
</template>

/* 这是组件内样式块，保留 scoped */
<style lang="scss" scoped>
/* === 布局：Header / Scroll / Footer 三段式 === */
.main {
  display: grid;
  grid-template-rows: auto 1fr auto; /* 头-中-尾 */
  height: 100dvh; /* 视口高度：移动端更稳 */
  box-sizing: border-box;
  padding: 20px;
  gap: 10px; /* 用 gap 代替子元素外边距，避免撑高 */
}

/* 顶部标题固定 */
.title {
  min-height: 60px; /* 固定高度 */
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;

  .leave-and-info {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  h2 {
    text-align: center;
    font-size: 20px;
  }

  p {
    font-size: 14px;
  }

  .roomId {
    display: flex;
    align-items: center;
    background-color: rgba(138, 138, 138, 0.1);
    padding: 7px;
    border-radius: 5px;

    button {
      margin-right: 7px;
      margin-left: 4px;
      font-size: 12px;
      background-color: transparent;
    }

    code {
      font-size: 16px;
      background-color: rgba(138, 138, 138, 0.3);
      padding: 5px;
      border-radius: 5px;
    }
  }
}

/* 中间聊天区：只在这里滚动 */
.chat {
  min-height: 0; /* 关键：允许在 grid/flex 中收缩 */
  display: flex;
  flex-direction: column;
  overflow: hidden; /* 自己不滚，内部滚 */
  width: 100%;

  .v-divider {
    margin: 10px 0;
    flex-shrink: 0;
  }

  .chat-messages {
    flex: 1;
    min-height: 0; /* 关键：让内部真正可滚 */
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
    padding: 10px 0;
  }

  .message-wrapper {
    margin-bottom: 12px;

    &.my-message {
      text-align: right;
    }
  }

  .message-bubble {
    display: inline-block;
    max-width: 70%;
    padding: 8px 12px;
    border-radius: 12px;
    margin: 2px 0;
  }

  .message-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 4px;
    font-size: 13px;
  }

  .message-sender {
    color: #1976d2;
    font-weight: 600;
  }

  .message-time {
    color: #666;
    font-size: 11px;
  }

  .message-text {
    font-size: 14px;
    line-height: 1.4;
    word-wrap: break-word;
    white-space: pre-wrap;
  }

  .my-message {
    .message-bubble {
      background-color: pink;
      border: 2px solid #a7a7a7;
    }

    .message-sender {
      color: #2e7d32;
    }
  }

  .message-wrapper:not(.my-message) .message-bubble {
    background-color: #f5f5f5;
    border: 1px solid #e0e0e0;
  }

  .no-messages {
    padding: 20px;
    color: #999;
    font-style: italic;
  }
}

/* 底部输入栏固定 */
.chat-input {
  min-height: 60px; /* 固定高度 */
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  width: 100%;

  /* 避免额外外边距把页面撑高，靠 .main 的 gap 控间距 */
  margin: 0;

  .v-input-field {
    align-self: center;
    margin: 0;
  }

  .v-icon {
    font-size: 28px;
  }
}
</style>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, computed, nextTick } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ws, connectWS } from "@/services/wsClient";

interface Room {
  id: string;
  players: string[];
  spectators: string[];
  roomStatus: string;
}

interface Message {
  playerName: string;
  message: string;
  timestamp?: Date;
}

const route = useRoute();
const router = useRouter();
const token = ref((route.query.token as string) || "");

const roomId = ref("");
const creator = ref("");
const currentRoom = ref<Room>({
  id: "",
  players: [],
  spectators: [],
  roomStatus: "waiting",
});
const chatInput = ref("");
const messages = ref<Message[]>([]);
const chatContainer = ref<HTMLElement>();
const refreshing = ref(false);

let roomListInterval: number | null = null;

// 格式化时间
function formatTime(date: Date): string {
  return new Date(date).toLocaleTimeString("zh-CN", {
    hour: "2-digit",
    minute: "2-digit",
  });
}

// 计算房间状态
const roomStatusColor = computed(() => {
  switch (currentRoom.value.roomStatus) {
    case "waiting":
      return "orange";
    case "playing":
      return "success";
    case "finished":
      return "grey";
    default:
      return "blue-grey";
  }
});
const roomStatusText = computed(() => {
  switch (currentRoom.value.roomStatus) {
    case "waiting":
      return "等待中";
    case "playing":
      return "游戏中";
    case "finished":
      return "已结束";
    default:
      return "未知";
  }
});

// 复制房间ID
function copyRoomId() {
  navigator.clipboard
    .writeText(roomId.value)
    .then(() => {
      alert("房间ID已复制");
    })
    .catch((err) => {
      console.error("复制失败：", err);
      alert("复制失败，请手动复制");
    });
}

// 通过token查询房间信息
const fetchRoomInfo = async () => {
  try {
    const response = await fetch(
      `http://api.gobang.lh520.pw/getRoomByToken?token=${token.value}`
    );
    const data = await response.json();

    if (!response.ok) {
      alert(data.error || "Token无效或已使用");
      router.push("/game/ol");
      return false;
    }

    roomId.value = data.roomId;
    creator.value = data.user;
    return true;
  } catch (error) {
    console.error("获取房间信息失败:", error);
    alert("获取房间信息失败，请返回重试");
    router.push("/game/ol");
    return false;
  }
};

// ---------------- WS 消息处理 ----------------
function handleWSMessage(msg: any) {
  const { action, payload } = msg;
  console.log("收到WebSocket消息:", action, payload);

  switch (action) {
    case "joinedRoom":
    case "roomCreated":
      if (payload.id === roomId.value || payload.roomId === roomId.value) {
        currentRoom.value = {
          id: payload.id || payload.roomId,
          players: payload.players || [],
          spectators: payload.spectators || [],
          roomStatus: payload.roomStatus || "waiting",
        };
        messages.value = (payload.messages || []).map((m: any) => ({
          playerName: m.playerName || m.sender || "未知用户",
          message: m.message || m.content || "",
          timestamp: m.timestamp ? new Date(m.timestamp) : new Date(),
        }));
        scrollToBottom();
      }
      break;
    case "roomUpdate":
      currentRoom.value.players = payload.players || [];
      currentRoom.value.spectators = payload.spectators || [];
      currentRoom.value.roomStatus = payload.roomStatus || "waiting";
      break;
    case "roomInfo":
      currentRoom.value.players = payload.players || [];
      currentRoom.value.spectators = payload.spectators || [];
      currentRoom.value.roomStatus = payload.roomStatus || "waiting";
      messages.value = (payload.messages || []).map((m: any) => ({
        playerName: m.playerName || m.sender || "未知用户",
        message: m.message || m.content || "",
        timestamp: m.timestamp ? new Date(m.timestamp) : new Date(),
      }));
      scrollToBottom();
      refreshing.value = false;
      break;
    case "newMessage":
      console.log("收到新消息:", payload);
      // 确保消息是针对当前房间的 - 放宽检查条件
      if (payload.roomId === roomId.value || !payload.roomId) {
        const existingMessage = messages.value.find(
          (m) =>
            m.playerName === (payload.playerName || payload.sender) &&
            m.message === (payload.message || payload.content) &&
            Math.abs(
              new Date(m.timestamp || Date.now()).getTime() -
                new Date(payload.timestamp || Date.now()).getTime()
            ) < 1000
        );

        if (!existingMessage) {
          messages.value.push({
            playerName: payload.playerName || payload.sender || "未知用户",
            message: payload.message || payload.content || "",
            timestamp: payload.timestamp
              ? new Date(payload.timestamp)
              : new Date(),
          });
          scrollToBottom();
        }
      }
      break;
    case "roomClosed":
      alert("房间已被关闭");
      router.push({ path: "/game/ol" });
      break;
    case "error":
      alert(payload);
      break;
  }
}

// ---------------- 房间信息 ----------------
function refreshRoomInfo() {
  if (!ws.value) return;
  refreshing.value = true;
  ws.value.send(
    JSON.stringify({ action: "getRoomInfo", payload: { roomId: roomId.value } })
  );
  setTimeout(() => (refreshing.value = false), 2000);
}

// ---------------- 聊天 ----------------
function scrollToBottom() {
  nextTick(() => {
    if (chatContainer.value)
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
  });
}

function sendMessage() {
  if (!chatInput.value.trim()) return;
  ws.value?.send(
    JSON.stringify({
      action: "sendMessage",
      payload: {
        roomId: roomId.value,
        playerName: creator.value,
        message: chatInput.value,
      },
    })
  );
  chatInput.value = "";
  scrollToBottom();
}

// ---------------- 离开 ----------------
function leaveRoom() {
  ws.value?.send(
    JSON.stringify({
      action: "leaveRoom",
      payload: { roomId: roomId.value, user: creator.value },
    })
  );
  router.push({ path: "/game/ol" });
}

// ---------------- 生命周期 ----------------
onMounted(async () => {
  console.log("play页面加载，token:", token.value);

  if (!token.value) {
    alert("Token缺失，请重新加入房间");
    router.push("/game/ol");
    return;
  }

  const roomInfoLoaded = await fetchRoomInfo();
  if (!roomInfoLoaded) return;

  // 添加消息监听器
  const messageHandler = (event: MessageEvent) => {
    const msg = JSON.parse(event.data);
    handleWSMessage(msg);
  };
  (ws.value as any)._messageHandler = messageHandler;
  ws.value?.addEventListener("message", messageHandler);

  // 通过Token加入房间
  ws.value?.send(
    JSON.stringify({
      action: "joinRoom",
      payload: { token: token.value },
    })
  );

  // 立即获取房间信息以确保消息同步
  setTimeout(() => {
    ws.value?.send(
      JSON.stringify({
        action: "getRoomInfo",
        payload: { roomId: roomId.value },
      })
    );
  }, 100);

  roomListInterval = window.setInterval(() => {
    ws.value?.send(
      JSON.stringify({
        action: "getRoomInfo",
        payload: { roomId: roomId.value },
      })
    );
  }, 5000);

  console.log("已连接，等待服务器推送房间信息...");
});

onBeforeUnmount(() => {
  if (roomListInterval) clearInterval(roomListInterval);
  if (ws.value && (ws.value as any)._messageHandler) {
    ws.value.removeEventListener("message", (ws.value as any)._messageHandler);
  }
});
</script>
