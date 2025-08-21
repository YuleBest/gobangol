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

      <div class="chat-messages">
        <div
          v-for="(msg, idx) in messages"
          :key="idx"
          class="message-wrapper"
          :class="{ 'my-message': msg.playerName === creator }"
        >
          <div class="message-bubble">
            <div class="message-avatar">
              <v-avatar
                size="32"
                :color="msg.playerName === creator ? 'success' : 'primary'"
                class="elevation-1"
              >
                <span class="white--text text-caption font-weight-bold">
                  {{ msg.playerName.charAt(0).toUpperCase() }}
                </span>
              </v-avatar>
            </div>
            <div class="message-content">
              <div class="message-header">
                <span class="message-sender font-weight-medium">
                  {{ msg.playerName }}
                </span>
                <span class="message-time text-caption grey--text">
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

<style lang="scss" scoped>
#app {
  height: 100%;
  width: 100%;
}

.main {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: 20px;
  height: calc(100% - 20px);
}

.title {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  // margin-bottom: 10px;
  height: 60px;

  .leave-and-info {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
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
    flex-direction: row;
    justify-content: center;
    align-items: center;
    background-color: rgba(138, 138, 138, 0.1);
    padding: 7px;
    border-radius: 5px;

    button {
      margin-right: 7px;
      margin-left: 4px;
      font-size: 12px;
      background-color: #00000000;
    }

    code {
      font-size: 16px;
      background-color: rgba(138, 138, 138, 0.3);
      padding: 5px;
      border-radius: 5px;
    }
  }
}

.chat {
  width: 100%;
  display: flex;
  flex-direction: column;
  flex: 1;

  .v-divider {
    margin: 10px 0;
  }

  .chat-messages {
    flex: 1;
  }
}

.chat-input {
  width: 100%;
  margin-bottom: 20px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: 10px;

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
import { ws } from "@/services/wsClient";

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
const creator = (route.query.creator as string) || "";
const roomId = (route.query.roomId as string) || "";
const joinToken = (route.query.joinToken as string) || ""; // 从URL或前端内存传入一次性token

const currentRoom = ref<Room>({
  id: roomId,
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
const roomStatusIcon = computed(() => {
  switch (currentRoom.value.roomStatus) {
    case "waiting":
      return "mdi-clock-outline";
    case "playing":
      return "mdi-play-circle";
    case "finished":
      return "mdi-check-circle";
    default:
      return "mdi-help-circle";
  }
});

// 复制房间ID
function copyRoomId() {
  const roomIdCode = document.querySelector("code");
  if (roomIdCode) {
    navigator.clipboard
      .writeText(roomId)
      .then(() => {
        alert("房间ID已复制");
      })
      .catch((err) => {
        console.error("复制失败：", err);
        alert("复制失败，请手动复制");
      });
  }
}
// ---------------- WS 消息处理 ----------------
function handleWSMessage(msg: any) {
  const { action, payload } = msg;
  switch (action) {
    case "joinedRoom":
    case "roomCreated":
      if (payload.id === roomId) {
        currentRoom.value = {
          id: payload.id,
          players: payload.players,
          spectators: payload.spectators,
          roomStatus: payload.roomStatus,
        };
        messages.value = (payload.messages || []).map((m: any) => ({
          ...m,
          timestamp: new Date(),
        }));
      }
      break;
    case "roomUpdate":
      currentRoom.value.players = payload.players;
      currentRoom.value.spectators = payload.spectators;
      currentRoom.value.roomStatus = payload.roomStatus;
      break;
    case "roomInfo":
      currentRoom.value.players = payload.players;
      currentRoom.value.spectators = payload.spectators;
      currentRoom.value.roomStatus = payload.roomStatus;
      refreshing.value = false;
      break;
    case "newMessage":
      messages.value.push({ ...payload, timestamp: new Date() });
      scrollToBottom();
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
  ws.value.send(JSON.stringify({ action: "getRoomInfo", payload: { roomId } }));
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
      payload: { roomId, playerName: creator, message: chatInput.value },
    })
  );
  chatInput.value = "";
  scrollToBottom();
}

// ---------------- 离开 ----------------
function leaveRoom() {
  ws.value?.send(
    JSON.stringify({ action: "leaveRoom", payload: { roomId, user: creator } })
  );
  router.push({ path: "/game/ol" });
}

// ---------------- 生命周期 ----------------
onMounted(() => {
  ws.value?.addEventListener("message", (event) => {
    const msg = JSON.parse(event.data);
    handleWSMessage(msg);
  });

  roomListInterval = window.setInterval(() => {
    // 可以周期性刷新房间信息
    ws.value?.send(
      JSON.stringify({ action: "getRoomInfo", payload: { roomId } })
    );
  }, 5000);

  if (roomId && creator) {
    const isCreator = route.query.isCreator === "true";

    if (isCreator) {
      // 创建者直接等待房间信息
      console.log("创建者进入房间，等待服务器推送房间信息");
    } else {
      // 加入者必须用一次性token
      if (!joinToken) {
        alert("加入房间失败：token缺失或已使用");
        router.push({ path: "/game/ol" });
      } else {
        ws.value?.send(
          JSON.stringify({
            action: "joinRoom",
            payload: { roomId, user: creator, password: "", joinToken },
          })
        );
      }
    }
  }
});

onBeforeUnmount(() => {
  if (roomListInterval) clearInterval(roomListInterval);
});
</script>
