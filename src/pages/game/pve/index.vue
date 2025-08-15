<template>
  <div class="main">
    <div class="container">
      <v-breadcrumbs :items="items">
        <template v-slot:prepend>
          <img src="/src/assets/logo.png" alt="logo" />
        </template>
      </v-breadcrumbs>
    </div>
    <div class="setting">
      <h1>选择难度</h1>
      <v-radio-group v-model="diffs" style="margin-top: 20px">
        <v-radio label="简单 (搜索深度 3)" value="simple"></v-radio>
        <v-radio label="中等 (搜索深度 5)" value="medium"></v-radio>
        <v-radio label="困难 (搜索深度 7)" value="hard"></v-radio>
        <v-radio label="专家 (搜索深度 9)" value="expert"></v-radio>
        <div style="color: red">
          <v-radio label="噩梦 (搜索深度 20 MAX)" value="nightmare"></v-radio>
        </div>
      </v-radio-group>
      <div class="start_game">
        <v-btn size="x-large" :to="`/game/pve/play?diff=${diffs}`"
          >开始游戏</v-btn
        >
      </div>
    </div>
  </div>
  <Footer />
</template>

<style scoped>
img {
  width: 20px;
  height: 20px;
  border-radius: 5px;
}

.container {
  height: 100px;
}

.setting {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.main {
  height: 100%;
  width: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.start_game {
  flex: 1;
}
</style>

<script setup>
const items = [
  {
    title: "五子棋在线",
    disabled: false,
    href: "/",
  },
  {
    title: "游戏",
    disabled: false,
    href: "/",
  },
  {
    title: "人机对弈",
    disabled: false,
    href: "/game/pve",
  },
];

import { ref } from "vue";

const diffs = ref("medium");
</script>
