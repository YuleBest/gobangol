<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import GameBodyPVE from '@/components/GameBodyPVE.vue'

const route = useRoute()

const displayDiff = computed(() => {
  const diff = route.query.diff
  switch (diff) {
    case 'simple':
      return '简单'
    case 'medium':
      return '中等'
    case 'hard':
      return '困难'
    case 'expert':
      return '专家'
    case 'nightmare':
      return '噩梦模式'
    default:
      return '未知'
  }
})
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
#app {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  margin: 0;
}

.all {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
}

.tips p {
  font-size: 10px;
  color: #666;
}

.tips {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-bottom: 10px;
}

.game {
  height: 95%;
  width: 95%;
  padding: 20px;
  /* flex: 1; */
}

.title {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 40px;
}

.title h1 {
  font-size: 24px;
}

.diff {
  display: flex;
  flex-direction: row;
  margin-bottom: 40px;
}

.diff .btn {
  margin: 0 10px;
}
</style>
