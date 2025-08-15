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
      <v-radio-group v-model="diffs">
        <v-radio label="简单（未开发）" value="simple"></v-radio>
        <v-radio label="中等" value="medium"></v-radio>
        <v-radio label="困难（未开发）" value="hard"></v-radio>
        <v-radio label="专家（未开发）" value="expert"></v-radio
        ><v-btn :to="`/game/pve/play?diff=${diffs}`">开始游戏</v-btn>
      </v-radio-group>
    </div>
  </div>
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
