<script lang="ts" setup>
import logo404 from "@/assets/image/404NotFound.png";
</script>

<template>
  <v-container
    class="fill-height d-flex flex-column align-center justify-center text-center"
  >
    <!-- Logo -->
    <img :src="logo404" style="width: 300px" />

    <!-- 主标题 -->
    <h1 class="display-2 font-weight-bold mb-2">页面未找到</h1>

    <!-- 副标题 -->
    <p class="subtitle-1 mb-6">抱歉，你访问的页面不存在或已被移除。</p>

    <!-- 返回首页按钮 -->
    <v-btn large to="/"> 返回首页 </v-btn>
  </v-container>
</template>

<style scoped>
p {
  color: var(--v-theme-on-background);
}
</style>
