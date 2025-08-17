<template>
  <Topbar />
  <div class="setting">
    <div class="title">
      <h1>设置</h1>
    </div>
    <div class="game-setting">
      <v-divider></v-divider>
      <h2>游戏设置</h2>
      <div class="music">
        <v-switch :model-value="true" label="开启音乐" inset></v-switch>
      </div>
      <div class="sound">
        <v-switch :model-value="true" label="开启音效" inset></v-switch>
      </div>
    </div>
    <div class="online-setting">
      <v-divider></v-divider>
      <h2>联机设置</h2>
      <div class="room">
        <v-switch
          :model-value="true"
          label="允许创建的房间展示在房间列表"
          inset
        ></v-switch>
      </div>
    </div>
  </div>
  <Footer />
</template>

<style scoped>
.setting {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: left;
  padding: 40px;
}

.setting h1 {
  font-size: 32px;
  font-weight: 500;
  margin-bottom: 20px;
}

.setting h2 {
  font-size: 24px;
  font-weight: 500;
  margin-bottom: 20px;
  margin-top: 20px;
}
</style>

<script setup>
import { useHead } from "@vueuse/head";
useHead({
  title: "设置 - GoBang OL",
  meta: [{ name: "description", content: "GoBang OL 设置" }],
});
</script>
