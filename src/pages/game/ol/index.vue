<template>
  <v-app>
    <!-- 全屏加载遮罩 -->
    <v-overlay
      v-model="showLoading"
      class="align-center justify-center"
      persistent
    >
      <div class="text-center">
        <Progress />
      </div>
    </v-overlay>

    <!-- 全屏错误提示 -->
    <v-overlay
      v-model="showError"
      class="align-center justify-center"
      persistent
    >
      <v-card class="pa-8 text-center" max-width="400">
        <v-icon color="error" size="64" class="mb-4">mdi-alert-circle</v-icon>
        <h2 class="mb-4">连接失败</h2>
        <p class="mb-6">服务器连接失败，请稍后再试</p>
        <v-btn to="/">回到主页</v-btn>
      </v-card>
    </v-overlay>

    <v-main>
      <v-container class="py-8" max-width="800px">
        <v-card elevation="5" class="pa-6">
          <h1 class="text-center">五子棋房间系统</h1>

          <!-- 初始界面：只显示两个按钮 -->
          <div v-if="currentStep === 'initial'" class="text-center">
            <v-row class="my-4">
              <v-col cols="12" md="6">
                <v-btn
                  color="primary"
                  size="large"
                  @click="startCreateRoom"
                  block
                >
                  <v-icon left>mdi-plus</v-icon>
                  创建房间
                </v-btn>
              </v-col>
              <v-col cols="12" md="6">
                <v-btn
                  color="success"
                  size="large"
                  @click="startJoinRoom"
                  block
                >
                  <v-icon left>mdi-login</v-icon>
                  加入房间
                </v-btn>
              </v-col>
            </v-row>

            <!-- 房间列表 -->
            <v-row class="mt-6">
              <v-col cols="12">
                <v-card variant="outlined" class="pa-4">
                  <div class="d-flex justify-space-between align-center mb-4">
                    <h3 class="text-h6">公开房间列表</h3>
                    <v-btn
                      color="primary"
                      variant="text"
                      size="small"
                      @click="getRoomList"
                      :disabled="!ws || ws.readyState !== 1"
                    >
                      <v-icon left size="small">mdi-refresh</v-icon>
                      刷新
                    </v-btn>
                  </div>

                  <div v-if="roomList.length === 0" class="text-center py-4">
                    <v-icon color="grey" size="48" class="mb-2"
                      >mdi-home-search</v-icon
                    >
                    <p class="text-grey">暂无公开房间</p>
                  </div>

                  <v-list v-else>
                    <v-list-item
                      v-for="room in roomList"
                      :key="room.id"
                      class="mb-2"
                      border
                    >
                      <template v-slot:prepend>
                        <v-icon color="primary">mdi-home</v-icon>
                      </template>

                      <v-list-item-title>
                        <strong>房间ID: {{ room.id }}</strong>
                      </v-list-item-title>

                      <v-list-item-subtitle>
                        <div>房主: {{ room.creator }}</div>
                        <div>玩家: {{ room.players.length }}/2</div>
                        <div>观众: {{ room.spectators.length }}</div>
                        <div>
                          状态:
                          <v-chip
                            size="x-small"
                            :color="
                              room.roomStatus === 'waiting' ? 'success' : 'info'
                            "
                          >
                            {{
                              room.roomStatus === "waiting"
                                ? "等待中"
                                : "观战中"
                            }}
                          </v-chip>
                        </div>
                      </v-list-item-subtitle>

                      <template v-slot:append>
                        <v-btn
                          color="success"
                          variant="outlined"
                          size="small"
                          @click="requestTokenAndJoin(room.id)"
                        >
                          加入
                        </v-btn>
                      </template>
                    </v-list-item>
                  </v-list>
                </v-card>
              </v-col>
            </v-row>
          </div>

          <!-- 创建房间表单 -->
          <div v-if="currentStep === 'create'">
            <h2 class="text-center mb-4">创建新房间</h2>
            <v-row class="my-4">
              <v-col cols="12">
                <v-text-field
                  v-model="creator"
                  label="你的昵称"
                  outlined
                  dense
                  :rules="[
                    (v) => !!v || '请输入昵称',
                    (v) =>
                      !/[\/\[\]*^@#<>|&$+={}]/g.test(v) ||
                      '昵称不能包含特殊符号',
                    (v) => (v && v.length <= 20) || '昵称长度不能超过20个字符',
                  ]"
                  required
                />
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="password"
                  label="房间密码（可选）"
                  outlined
                  dense
                  type="password"
                  hint="留空表示创建公开房间"
                />
              </v-col>
              <v-col cols="12" class="d-flex justify-space-between">
                <v-btn color="grey" @click="backToInitial">返回</v-btn>
                <v-btn
                  color="primary"
                  @click="handleCreateRoom"
                  :disabled="!creator"
                  >创建房间</v-btn
                >
              </v-col>
            </v-row>
          </div>

          <!-- 加入房间表单 -->
          <div v-if="currentStep === 'join'">
            <h2 class="text-center mb-4">加入房间</h2>
            <v-row class="my-4">
              <v-col cols="12">
                <v-text-field
                  v-model="creator"
                  label="你的昵称"
                  :rules="[
                    (v) => !!v || '请输入昵称',
                    (v) =>
                      !/[\/\[\]*^@#<>|&$+={}]/g.test(v) ||
                      '昵称不能包含特殊符号',
                    (v) => (v && v.length <= 20) || '昵称长度不能超过20个字符',
                  ]"
                  required
                />
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="joinRoomId"
                  label="房间ID"
                  outlined
                  dense
                  :rules="[(v) => !!v || '请输入房间ID']"
                  required
                />
              </v-col>
              <v-col cols="12" v-if="showJoinPassword">
                <v-text-field
                  v-model="joinRoomPassword"
                  label="房间密码"
                  outlined
                  dense
                  type="password"
                  :rules="[(v) => !!v || '请输入房间密码']"
                  required
                />
              </v-col>
              <v-col cols="12" v-if="joinError" class="text-center">
                <v-alert type="error" variant="tonal" class="mb-4">
                  {{ joinError }}
                </v-alert>
              </v-col>
              <v-col cols="12" class="d-flex justify-space-between">
                <v-btn color="grey" @click="backToInitial">返回</v-btn>
                <v-btn
                  color="success"
                  @click="requestTokenAndJoin(joinRoomId.trim())"
                  :disabled="
                    !creator ||
                    !joinRoomId ||
                    (showJoinPassword && !joinRoomPassword)
                  "
                >
                  加入房间
                </v-btn>
              </v-col>
            </v-row>
          </div>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { ws, connectWS } from "@/services/wsClient";
import { useRouter } from "vue-router";

interface Room {
  id: string;
  creator: string;
  players: string[];
  spectators: string[];
  roomStatus: string;
}

// ---------- 状态 ----------
const creator = ref("");
const password = ref("");
const joinRoomId = ref("");
const joinRoomPassword = ref("");
const showLoading = ref(true);
const showError = ref(false);
const currentStep = ref<"initial" | "create" | "join">("initial");
const showJoinPassword = ref(false);
const joinError = ref("");
const roomList = ref<Room[]>([]);
const showRoomList = ref(false);

const joinToken = ref(""); // 内存保存 token

const router = useRouter();

// ---------------- 初始化 WS ----------------
onMounted(() => {
  connectWS(
    "ws://api.gobang.lh520.pw/ws",
    () => {
      showLoading.value = false;
      getRoomList();
    },
    () => {
      showLoading.value = false;
      showError.value = true;
    }
  );

  // 连接超时处理
  setTimeout(() => {
    if (showLoading.value && (!ws.value || ws.value.readyState !== 1)) {
      showLoading.value = false;
      showError.value = true;
    }
  }, 5000);
});

// ---------------- 获取房间列表 ----------------
function getRoomList() {
  if (!ws.value || ws.value.readyState !== 1) return;
  const listener = (event: MessageEvent) => {
    const msg = JSON.parse(event.data);
    if (msg.action === "roomList") {
      roomList.value = msg.payload;
      ws.value?.removeEventListener("message", listener);
    }
  };
  ws.value.addEventListener("message", listener);
  ws.value.send(JSON.stringify({ action: "getRoomList" }));
}

// ---------------- 验证昵称 ----------------
function validateNickname(nickname: string): string | true {
  const specialChars = /[/\[\]*^@#<>|"'&$+={}]/;
  if (specialChars.test(nickname))
    return "昵称不能包含特殊符号: /[]*^@#<>|'&$+={}";
  if (nickname.length < 1 || nickname.length > 20)
    return "昵称长度必须在1-20个字符之间";
  return true;
}

// ---------------- 步骤控制 ----------------
function startCreateRoom() {
  currentStep.value = "create";
  creator.value = "";
  password.value = "";
}

function startJoinRoom() {
  currentStep.value = "join";
  creator.value = "";
  joinRoomId.value = "";
  joinRoomPassword.value = "";
  showJoinPassword.value = false;
  joinError.value = "";
}

function backToInitial() {
  currentStep.value = "initial";
  creator.value = "";
  password.value = "";
  joinRoomId.value = "";
  joinRoomPassword.value = "";
  showJoinPassword.value = false;
  joinError.value = "";
  joinToken.value = "";
}

// ---------------- 创建房间 ----------------
function handleCreateRoom() {
  if (!creator.value) return alert("请输入昵称");
  const nicknameValidation = validateNickname(creator.value);
  if (nicknameValidation !== true) return alert(nicknameValidation);
  if (!ws.value || ws.value.readyState !== 1)
    return alert("WebSocket 尚未连接，请稍等...");

  const listener = (event: MessageEvent) => {
    const msg = JSON.parse(event.data);
    console.log("创建房间收到消息:", msg);
    if (msg.action === "roomCreated" && msg.payload.token) {
      console.log("房间创建成功，收到token:", msg.payload.token);
      const token = msg.payload.token;
      ws.value?.removeEventListener("message", listener);
      router.push({
        path: "/game/ol/play-copy",
        query: { token }, // 只传递token
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

// ---------------- 请求临时 token 并加入房间 ----------------
function requestTokenAndJoin(roomId: string) {
  console.log("开始请求token，房间ID:", roomId, "用户:", creator.value);

  // 保存房间ID，无论是否有昵称都先请求token
  joinRoomId.value = roomId;

  if (!creator.value) {
    console.log("用户昵称为空，跳转到加入房间页面填写昵称");
    currentStep.value = "join";
    return;
  }

  const nicknameValidation = validateNickname(creator.value);
  if (nicknameValidation !== true) {
    console.log("昵称验证失败:", nicknameValidation);
    currentStep.value = "join";
    return;
  }

  if (!ws.value || ws.value.readyState !== 1) {
    console.error("WebSocket未连接，状态:", ws.value?.readyState);
    return alert("WebSocket 尚未连接，请稍等...");
  }

  const tokenListener = (event: MessageEvent) => {
    console.log("收到WebSocket消息:", event.data);
    const msg = JSON.parse(event.data);
    console.log("解析后的消息:", msg);

    if (msg.action === "joinToken" && msg.payload.token) {
      console.log("收到加入token:", msg.payload.token);
      const token = msg.payload.token;
      ws.value?.removeEventListener("message", tokenListener);
      router.push({
        path: "/game/ol/play-copy",
        query: { token }, // 只传递token
      });
    } else if (msg.action === "error") {
      console.error("收到错误消息:", msg.payload);
      alert(msg.payload);
      ws.value?.removeEventListener("message", tokenListener);
    } else {
      console.log("收到其他类型消息:", msg.action, msg.payload);
    }
  };

  ws.value.addEventListener("message", tokenListener);

  ws.value.send(
    JSON.stringify({
      action: "requestJoinToken",
      payload: {
        roomId,
        user: creator.value,
        password: joinRoomPassword.value,
      },
    })
  );
}

// 这个函数现在被requestTokenAndJoin替代，不再直接使用
</script>
