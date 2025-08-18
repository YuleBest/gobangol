<template>
  <v-app>
    <v-main>
      <v-container class="py-8" max-width="900px">
        <v-card elevation="5" class="pa-6">
          <v-row>
            <v-col cols="12">
              <h1 class="text-center">管理员房间管理</h1>
            </v-col>
          </v-row>

          <!-- 登录 -->
          <v-row v-if="!loggedIn" class="my-4">
            <v-col cols="12" md="6">
              <v-text-field
                v-model="username"
                label="账号"
                outlined
                dense
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="password"
                label="密码"
                type="password"
                outlined
                dense
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-btn color="primary" @click="handleLogin">登录</v-btn>
            </v-col>
          </v-row>

          <!-- 房间列表 -->
          <v-row v-if="loggedIn">
            <v-col cols="12">
              <h2>所有房间</h2>
              <v-list two-line>
                <v-list-item v-for="room in rooms" :key="room.id">
                  <v-list-item-content>
                    <v-list-item-title>
                      房间: {{ room.id }} (创建者: {{ room.creator }})
                    </v-list-item-title>
                    <v-list-item-subtitle>
                      玩家: {{ room.players.join(", ") }} | 观众:
                      {{ room.spectators.join(", ") }} | 密码:
                      {{ room.password || "无" }} | 状态: {{ room.roomStatus }}
                    </v-list-item-subtitle>
                  </v-list-item-content>
                  <v-list-item-action>
                    <v-btn small color="error" @click="destroyRoom(room.id)"
                      >销毁</v-btn
                    >
                  </v-list-item-action>
                </v-list-item>
              </v-list>
            </v-col>
          </v-row>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from "vue";

const username = ref("");
const password = ref("");
const loggedIn = ref(false);

const rooms = ref<any[]>([]);
let ws: WebSocket | null = null;
let roomListInterval: any = null;

function connectWS() {
  ws = new WebSocket("ws://api.gobang.lh520.pw/ws");

  ws.onopen = () => {
    console.log("[WS] 已连接");
    fetchRoomList();
    roomListInterval = setInterval(fetchRoomList, 5000);
  };
  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    handleWSMessage(msg);
  };
  ws.onclose = () => {
    console.log("[WS] 已断开");
    if (roomListInterval) clearInterval(roomListInterval);
  };
}

function handleWSMessage(msg: any) {
  const { action, payload } = msg;
  switch (action) {
    case "roomList":
      rooms.value = payload;
      break;
    case "roomClosed":
      fetchRoomList();
      break;
    case "error":
      alert(payload);
      break;
  }
}

function fetchRoomList() {
  if (!ws) return;
  ws.send(JSON.stringify({ action: "getRoomList", payload: { admin: true } }));
}

function handleLogin() {
  if (username.value === "admin" && password.value === "admin") {
    loggedIn.value = true;
    connectWS();
  } else {
    alert("账号或密码错误");
  }
}

function destroyRoom(roomId: string) {
  if (!ws) return;
  ws.send(JSON.stringify({ action: "destroyRoom", payload: { roomId } }));
}

onBeforeUnmount(() => {
  if (roomListInterval) clearInterval(roomListInterval);
  if (ws) ws.close();
});
</script>

<style scoped>
.v-list-item {
  border-bottom: 1px solid #ccc;
}
</style>
