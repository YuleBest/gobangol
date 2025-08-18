<template>
  <div class="all">
    <div class="title">
      <h1>双人对弈</h1>
      <p v-if="enabledForbiddenMoves.length > 0">
        # 禁手启用：{{ enabledForbiddenMoves.join("、") }}
      </p>
      <p v-if="route.query.swap2 === 'true'"># Swap2 启用</p>
      <p v-if="route.query.allowUndo === 'true'"># 悔棋 启用</p>
    </div>
    <div class="game">
      <GameBodyPVP
        :doubleThree="route.query.doubleThree === 'true'"
        :doubleFour="route.query.doubleFour === 'true'"
        :longConnect="route.query.longConnect === 'true'"
        :swap2="route.query.swap2 === 'true'"
        :allowUndo="route.query.allowUndo === 'true'"
      />
    </div>
    <div class="tips">
      <p>点击两次棋盘上的位置下棋</p>
      <p>PC 端可使用 Ctrl + 鼠标滚轮进行缩放</p>
      <p>移动端可使用双指放大缩小进行缩放</p>
    </div>
    <div class="diff">
      <div class="btn">
        <v-btn to="/"><v-icon>mdi-home</v-icon>返回首页</v-btn>
      </div>
      <div class="btn">
        <v-btn to="/game/pvp"><v-icon>mdi-cog</v-icon>棋局设置</v-btn>
      </div>
    </div>
  </div>
  <Footer />
</template>

<style scoped>
@import "@/assets/style/playpages-PVPandPVE.css";
.game {
  margin: -50px 0;
}

.title p {
  font-size: 13px;
  color: rgba(229, 255, 0, 0.925);
}
</style>

<script setup>
import { useHead } from "@vueuse/head";
import { useRoute } from "vue-router";
import { computed } from "vue";

const route = useRoute();

const enabledForbiddenMoves = computed(() => {
  const forbidden = [];
  if (route.query.doubleThree === "true") forbidden.push("三三禁手");
  if (route.query.doubleFour === "true") forbidden.push("四四禁手");
  if (route.query.longConnect === "true") forbidden.push("长连禁手");
  return forbidden;
});

useHead({
  title: "双人对弈 - Gobang OL",
  meta: [{ name: "description", content: "Gobang OL 双人对弈（PVP）" }],
});
</script>
