<template>
  <v-app>
    <v-main>
      <v-container class="py-8" max-width="800px">
        <v-card elevation="5" class="pa-6">
          <h1 class="text-center">房间: {{ roomId }}</h1>

          <p>玩家: {{ currentRoom.players.join(", ") }}</p>
          <p>观众: {{ currentRoom.spectators.join(", ") }}</p>
          <p>状态: {{ currentRoom.roomStatus }}</p>

          <!-- 聊天 -->
          <v-divider class="my-3"></v-divider>
          <h3>聊天</h3>
          <div class="chat-box">
            <div v-for="(msg, idx) in messages" :key="idx">
              <strong>{{ msg.playerName }}:</strong> {{ msg.message }}
            </div>
          </div>

          <v-text-field
            v-model="chatInput"
            label="输入消息..."
            dense
            outlined
            @keyup.enter="sendMessage"
          />
          <div class="center">
            <v-btn color="primary" @click="sendMessage">发送</v-btn>
            <v-btn color="secondary" class="mt-3" @click="leaveRoom"
              >离开房间</v-btn
            >
          </div>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ws, fetchRoomList } from "@/services/wsClient";

interface Room {
  id: string;
  players: string[];
  spectators: string[];
  roomStatus: string;
}

interface Message {
  playerName: string;
  message: string;
}

const route = useRoute();
const router = useRouter();
const creator = (route.query.creator as string) || "";
const roomId = (route.query.roomId as string) || "";

const currentRoom = ref<Room>({
  id: roomId,
  players: [],
  spectators: [],
  roomStatus: "waiting",
});
const chatInput = ref("");
const messages = ref<Message[]>([]);

let roomListInterval: number | null = null;

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
        messages.value = payload.messages || [];
      }
      break;
    case "roomUpdate":
      currentRoom.value.players = payload.players;
      currentRoom.value.spectators = payload.spectators;
      currentRoom.value.roomStatus = payload.roomStatus;
      break;
    case "newMessage":
      messages.value.push(payload);
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

// ---------------- 聊天 ----------------
function sendMessage() {
  if (!chatInput.value.trim()) return;
  ws.value?.send(
    JSON.stringify({
      action: "sendMessage",
      payload: { roomId, playerName: creator, message: chatInput.value },
    })
  );
  chatInput.value = "";
}

function leaveRoom() {
  ws.value?.send(
    JSON.stringify({
      action: "leaveRoom",
      payload: { roomId, user: creator },
    })
  );
  router.push({ path: "/game/ol" });
}

// ---------------- 生命周期 ----------------
onMounted(() => {
  ws.value?.addEventListener("message", (event) => {
    const msg = JSON.parse(event.data);
    handleWSMessage(msg);
  });

  roomListInterval = window.setInterval(fetchRoomList, 5000);

  if (roomId && creator) {
    ws.value?.send(
      JSON.stringify({
        action: "joinRoom",
        payload: { roomId, user: creator, password: "" },
      })
    );
  }
});

onBeforeUnmount(() => {
  if (roomListInterval) clearInterval(roomListInterval);
});
</script>

<style scoped>
.chat-box {
  border: 1px solid #ccc;
  height: 200px;
  overflow-y: auto;
  padding: 10px;
  margin-bottom: 10px;
  background: #f9f9f900;
}

.center {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.center * {
  margin: 0 5px;
}
</style>
