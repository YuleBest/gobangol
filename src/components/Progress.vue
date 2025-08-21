<template>
  <div class="main">
    <div class="progress">
      <v-progress-circular indeterminate></v-progress-circular>
    </div>
    <div class="text">连接服务器中...</div>
  </div>
</template>

<style scoped>
.main {
  display: flex;
  flex-direction: row;
  align-items: center;
}

.progress {
  margin: 10px;
}

.text {
  font-size: 16px;
  font-weight: 500;
}
</style>
