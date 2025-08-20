<template>
  <v-app>
    <v-main>
      <v-card-text>
        <v-row>
          <v-col cols="12" md="8">
            <div class="d-flex align-center mb-3">
              <div class="text-h6 font-weight-medium">游戏聊天</div>
              <v-spacer></v-spacer>
              <v-btn
                icon
                size="small"
                variant="text"
                @click="refreshRoomInfo"
                :loading="refreshing"
                title="刷新房间信息"
              >
                <v-icon>mdi-refresh</v-icon>
              </v-btn>
            </div>
            <v-card
              elevation="2"
              class="chat-container rounded-lg pa-2"
              ref="chatContainer"
            >
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
                        :color="
                          msg.playerName === creator ? 'success' : 'primary'
                        "
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
            </v-card>
          </v-col>
          <v-col cols="12" md="4">
            <div class="text-h6 mb-3 font-weight-medium">
              游戏信息
              <v-chip class="font-weight-bold" small>
                <v-icon left small>{{ roomStatusIcon }}</v-icon>
                {{ roomStatusText }}
              </v-chip>
            </div>
            <v-card elevation="2" class="rounded-lg pa-4">
              <div class="text-body-2">
                <div class="d-flex justify-space-between mb-2">
                  <span>房间ID:</span>
                  <v-chip small color="grey lighten-2">{{ roomId }}</v-chip>
                </div>
                <div class="d-flex justify-space-between mb-2">
                  <span>当前玩家:</span>
                </div>
                <div class="d-flex justify-space-between">
                  <span>当前观众: </span>
                  <span class="font-weight-medium">{{
                    currentRoom.spectators.length
                  }}</span>
                </div>
              </div>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions class="px-6 py-4">
        <v-row no-gutters align="center">
          <v-col cols="12" md="9">
            <v-text-field
              v-model="chatInput"
              label="输入消息..."
              outlined
              dense
              hide-details
              prepend-inner-icon="mdi-message-text"
              class="mr-3"
              @keyup.enter="sendMessage"
            />
          </v-col>
          <v-col cols="12" md="3" class="d-flex justify-end">
            <v-btn
              color="primary"
              large
              elevation="2"
              :disabled="!chatInput.trim()"
              @click="sendMessage"
              class="mr-2"
            >
              <v-icon left>mdi-send</v-icon>
              发送
            </v-btn>
            <v-btn color="error" large outlined @click="leaveRoom">
              <v-icon left>mdi-exit-to-app</v-icon>
              离开
            </v-btn>
          </v-col>
        </v-row>
      </v-card-actions>
      <!-- </v-card> -->
      <!-- </v-container> -->
    </v-main>
  </v-app>
</template>

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

<style scoped>
.chat-container {
  height: 400px;
  overflow-y: auto;
  background: #f5f5f5;
}

.chat-messages {
  padding: 8px;
}

.message-wrapper {
  margin-bottom: 12px;
  display: flex;
  align-items: flex-start;
}

.message-bubble {
  display: flex;
  max-width: 70%;
  align-items: flex-start;
}

.message-avatar {
  margin-right: 8px;
  flex-shrink: 0;
}

.message-content {
  flex: 1;
  min-width: 0;
}

.message-header {
  display: flex;
  align-items: center;
  margin-bottom: 2px;
  gap: 8px;
}

.message-sender {
  font-size: 0.75rem;
  color: #1976d2;
}

.message-time {
  font-size: 0.7rem;
  color: #666;
}

.message-text {
  background: white;
  padding: 8px 12px;
  border-radius: 18px;
  display: inline-block;
  max-width: 100%;
  word-wrap: break-word;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  font-size: 0.875rem;
  line-height: 1.4;
  color: #000000;
}

.others-message-text {
  color: #000000;
  background: #ffffff;
  border: 1px solid #e0e0e0;
}

.my-message {
  justify-content: flex-end;
}

.my-message .message-bubble {
  flex-direction: row-reverse;
}

.my-message .message-avatar {
  margin-right: 0;
  margin-left: 8px;
}

.my-message .message-content {
  text-align: right;
}

.my-message .message-sender {
  color: #388e3c;
}

.my-message-text {
  background: #e3f2fd;
  color: #1976d2;
  border-radius: 18px 18px 0 18px;
}

@media (max-width: 960px) {
  .chat-container {
    height: 300px;
  }

  .message-bubble {
    max-width: 85%;
  }
}

.message-wrapper:last-child {
  margin-bottom: 0;
}
</style>
