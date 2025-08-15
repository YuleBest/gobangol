<template>
  <div class="main">
    <div class="game">
      <div class="title">
        <v-btn to="/"><v-icon>mdi-arrow-left</v-icon>返回首页</v-btn>
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
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
