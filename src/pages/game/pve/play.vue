<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import GameBodyPVE from "@/components/GameBodyPVE.vue";

const route = useRoute();

const gameId = ref("");

const generateGameId = () => {
  const diff = route.query.diff as string;
  const timestamp = Date.now();
  const combinedString = `${diff}-${timestamp}`;
  let hash = 0;
  for (let i = 0; i < combinedString.length; i++) {
    const char = combinedString.charCodeAt(i);
    hash = (hash << 5) - hash + char;
    hash |= 0;
  }
  const rawHash = Math.abs(hash).toString(36);
  gameId.value = `${rawHash.slice(0, 14)}|${timestamp}|${diff}`;
};

onMounted(() => {
  generateGameId();
});

const displayDiff = computed(() => {
  const diff = route.query.diff;
  switch (diff) {
    case "simple":
      return "简单";
    case "medium":
      return "中等";
    case "hard":
      return "困难";
    case "expert":
      return "专家";
    case "nightmare":
      return "噩梦模式";
    default:
      return "未知";
  }
});

import { useHead } from "@vueuse/head";
useHead({
  title: "人机对弈 - Gobang OL",
  meta: [{ name: "description", content: "Gobang OL 人机对弈（PVE）" }],
});
</script>

<template>
  <div class="all">
    <div class="title">
      <h1>人机对弈</h1>
      <p>难度：{{ displayDiff }}</p>
    </div>
    <div class="game">
      <GameBodyPVE :difficulty="route.query.diff as string" />
    </div>
    <div class="tips">
      <p>点击两次棋盘上的位置下棋</p>
      <p>PC 端可使用 Ctrl + 鼠标滚轮进行缩放</p>
      <p>移动端可使用双指放大缩小进行缩放</p>
      <div class="gameid">
        <p>对局ID: {{ gameId }}</p>
      </div>
    </div>
    <div class="diff">
      <div class="btn">
        <v-btn to="/"><v-icon>mdi-home</v-icon>返回首页</v-btn>
      </div>
      <div class="btn">
        <v-btn to="/game/pve"><v-icon>mdi-arrow-left</v-icon>选择难度</v-btn>
      </div>
    </div>
  </div>
  <Footer />
</template>

<style scoped>
@import "@/assets/style/playpages-PVPandPVE.css";
.game {
  margin: -40px 0;
}
</style>
