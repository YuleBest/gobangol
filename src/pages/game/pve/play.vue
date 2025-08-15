<template>
  <div class="main">
    <div class="game">
      <div class="title">
        <v-btn to="/"><v-icon>mdi-arrow-left</v-icon>返回首页</v-btn>
        <h1>人机对弈</h1>
        <p>难度：{{ $route.query.diff }}</p>
      </div>
      <GameBodyPVE />
    </div>
  </div>
</template>

<style scoped>
.main {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.game {
  height: 95%;
  width: 95%;
  padding: 20px;
}

.title {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
  margin-bottom: -20px;
}
</style>
