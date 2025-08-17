<template>
  <div class="main">
    <div class="container">
      <v-breadcrumbs :items="items">
        <template v-slot:prepend>
          <div class="logo">
            <a href="/">
              <!-- 白色 logo，深色模式显示 -->
              <img
                v-show="isDarkMode"
                class="site-logo light"
                :src="logoWhite"
                alt="logo"
              />
              <!-- 黑色 logo，浅色模式显示，放大 15% -->
              <img
                v-show="!isDarkMode"
                class="site-logo dark"
                :src="logoBlack"
                alt="logo"
              />
            </a>
          </div>
        </template>
      </v-breadcrumbs>
    </div>
    <div class="setting">
      <h1>选择难度</h1>
      <v-radio-group v-model="diffs" style="margin-top: 20px">
        <v-radio label="简单 (搜索深度 3)" value="simple"></v-radio>
        <v-radio label="中等 (搜索深度 5)" value="medium"></v-radio>
        <v-radio label="困难 (搜索深度 7)" value="hard"></v-radio>
        <v-radio label="专家 (搜索深度 9)" value="expert"></v-radio>
        <div style="color: red">
          <v-radio label="噩梦 (搜索深度 20 MAX)" value="nightmare"></v-radio>
        </div>
      </v-radio-group>
      <div class="start_game">
        <v-btn size="x-large" :to="`/game/pve/play?diff=${diffs}`"
          >开始游戏</v-btn
        >
      </div>
    </div>
  </div>
  <Footer />
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useTheme } from "vuetify";

// 图片 import
import logoWhite from "@/assets/image/logo_white.png";
import logoBlack from "@/assets/image/logo_black.png";

const items = [
  { title: "", disabled: false, href: "/" },
  { title: "游戏", disabled: false, href: "/" },
  { title: "人机对弈", disabled: false, href: "/game/pve" },
];

const diffs = ref("medium");

const theme = useTheme();

// 初始化主题
onMounted(() => {
  const saved = localStorage.getItem("themeMode");
  if (saved === "light" || saved === "dark" || saved === "system") {
    theme.change(saved);
  }
});

// 是否为深色模式
const isDarkMode = ref(theme.global.current.value.dark);

// 监听 theme 变化
watch(
  () => theme.global.current.value,
  (val) => {
    isDarkMode.value = val.dark;
  },
  { deep: true, immediate: true }
);

import { useHead } from "@vueuse/head";
useHead({
  title: "人机对弈 - 选择难度 - GoBang OL",
  meta: [
    { name: "description", content: "GoBang OL 人机对弈（PVE）- 选择难度" },
  ],
});
</script>

<style scoped>
.site-logo {
  height: 15px;
}

/* 浅色模式 logo 放大 15% */
.site-logo.dark {
  transform: scale(1.15);
  transform-origin: left center;
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

.start_game {
  flex: 1;
}
</style>
