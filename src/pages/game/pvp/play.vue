<template>
  <div class="all">
    <div class="title">
      <h1>双人对弈</h1>
    </div>
    <div class="game">
      <GameBodyPVP />
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
    </div>
  </div>
  <Footer />
</template>

<style scoped>
@import "@/assets/style/playpages-PVPandPVE.css";
</style>
