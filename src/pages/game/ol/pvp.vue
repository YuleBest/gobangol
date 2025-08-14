<template>
  <Topbar />
  <v-divider></v-divider>
  <div class="main">
    <!-- 房间信息 -->
    <div class="room_info">
      <v-app-bar :elevation="0">
        <template v-slot:prepend>
          <v-btn width="30px" height="30px" to="/">
            <v-icon font-size="20px">mdi-arrow-left</v-icon>
          </v-btn>
        </template>

        <v-app-bar-title>Yule 的房间</v-app-bar-title>

        <template v-slot:append>
          <div class="room_id_band">
            <v-chip> ID </v-chip>
            <v-btn @click="copyRoomID"> {{ roomID }} </v-btn>
          </div>
        </template>
      </v-app-bar>
    </div>
    <!-- 游戏本体 -->
    <div class="game_body">
      <h1>游戏待开发</h1>
    </div>
    <Chat />
  </div>

  <Footer />
</template>

<style scoped>
.main {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}

.game_body {
  flex: 1;
}
</style>

<script setup>
import { ref } from "vue";
import { ElMessage } from "element-plus";
import { useClipboard } from "@vueuse/core";

const roomID = ref("123456");
const { copy } = useClipboard();

const copyRoomID = () => {
  try {
    copy(roomID.value);
    ElMessage.success("复制成功");
  } catch (error) {
    ElMessage.error("复制失败");
  }
};
</script>
