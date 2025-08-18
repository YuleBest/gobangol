<template>
  <v-app>
    <v-main>
      <v-container class="py-8" max-width="800px">
        <v-card elevation="5" class="pa-6">
          <h1 class="text-center">五子棋房间系统</h1>

          <!-- 创建房间 -->
          <v-row class="my-4">
            <v-col cols="12" md="6">
              <v-text-field v-model="creator" label="你的昵称" outlined dense />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="password"
                label="房间密码（可选）"
                outlined
                dense
              />
            </v-col>
            <v-col cols="12">
              <v-btn color="primary" @click="handleCreateRoom">创建房间</v-btn>
            </v-col>
          </v-row>

          <!-- 加入房间 -->
          <v-row class="my-4">
            <v-col cols="12" md="4">
              <v-text-field
                v-model="joinRoomId"
                label="房间ID"
                outlined
                dense
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="joinRoomPassword"
                label="房间密码（如有）"
                outlined
                dense
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-btn color="success" @click="handleJoinRoom">加入房间</v-btn>
            </v-col>
          </v-row>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { ws, connectWS } from "@/services/wsClient";
import { useRouter } from "vue-router";

const creator = ref("");
const password = ref("");
const joinRoomId = ref("");
const joinRoomPassword = ref("");

const router = useRouter();

// ---------------- 初始化 WS ----------------
onMounted(() => {
  connectWS("ws://api.gobang.lh520.pw/ws");
});

// ---------------- 创建房间 ----------------
function handleCreateRoom() {
  if (!creator.value) return alert("请输入昵称");

  if (!ws.value || ws.value.readyState !== WebSocket.OPEN) {
    return alert("WebSocket 尚未连接，请稍等...");
  }

  const listener = (event: MessageEvent) => {
    const msg = JSON.parse(event.data);
    if (msg.action === "roomCreated" && msg.payload.creator === creator.value) {
      const roomId = msg.payload.id;
      ws.value?.removeEventListener("message", listener);
      router.push({
        path: "/game/ol/play",
        query: { creator: creator.value, roomId },
      });
    }
  };

  ws.value.addEventListener("message", listener);

  ws.value.send(
    JSON.stringify({
      action: "createRoom",
      payload: { creator: creator.value, password: password.value || "" },
    })
  );
}

// ---------------- 加入房间 ----------------
function handleJoinRoom() {
  if (!creator.value) return alert("请输入昵称");
  const id = joinRoomId.value;
  if (!id) return alert("请输入房间ID");

  if (!ws.value || ws.value.readyState !== WebSocket.OPEN) {
    return alert("WebSocket 尚未连接，请稍等...");
  }

  ws.value.send(
    JSON.stringify({
      action: "joinRoom",
      payload: {
        roomId: id,
        user: creator.value,
        password: joinRoomPassword.value || "",
      },
    })
  );

  router.push({
    path: "/game/ol/play",
    query: { creator: creator.value, roomId: id },
  });
}
</script>
