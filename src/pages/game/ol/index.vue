<template>
  <Topbar />
  <v-divider></v-divider>
  <div class="main">
    <div class="title">
      <h1>联机对弈</h1>
      <p>与好友进行对弈，挑战各路棋士</p>
    </div>
    <div class="starter">
      <v-btn class="mt-2" type="submit" width="300px" to="/game/ol/pvp" block>
        创建房间
      </v-btn>
      <p>或</p>
      <div class="join">
        <v-text-field
          v-model="room_id"
          :rules="rules"
          width="300px"
          label="输入房间号进入房间"
        ></v-text-field>
        <v-btn class="mt-2" type="submit" block>确认</v-btn>
      </div>
    </div>
  </div>
  <Footer />
</template>

<style scoped>
.main {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.title {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-bottom: 40px;
}

.title p {
  font-size: 14px;
  color: #999;
}

.starter {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.starter p {
  font-size: 14px;
  color: #999;
  margin: 15px;
}

.join {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>

<script lang="ts" setup>
import { ref } from "vue";

const room_id = ref("");

const rules = [
  (value: string) => {
    if (value) return true;
    return "房间号不存在";
  },
];

import { useHead } from "@vueuse/head";
useHead({
  title: "联机对弈 - Gobang OL",
  meta: [{ name: "description", content: "Gobang OL 联机对弈" }],
});
</script>
