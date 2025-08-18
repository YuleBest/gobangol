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
              <!-- 黑色 logo，浅色模式显示 -->
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
      <h1>棋局设置</h1>
      <div class="setting-items">
        <!-- 棋局设置 START -->
        <div class="setting-item">
          <div class="setting-item-title">
            <h4>禁手设置</h4>
          </div>
          <div class="setting-item-content">
            <v-switch
              label="三三禁手"
              inset
              color="blue"
              v-model="doubleThree"
            ></v-switch>
            <v-switch
              label="四四禁手"
              inset
              color="blue"
              v-model="doubleFour"
            ></v-switch>
            <v-switch
              label="长连禁手"
              inset
              color="blue"
              v-model="longConnect"
            ></v-switch>
          </div>
        </div>
        <!-- 棋局设置 END -->
      </div>
      <a
        class="link"
        href="https://baike.baidu.com/item/%E7%A6%81%E6%89%8B/214940"
        target="_blank"
        >什么是禁手
      </a>
      <div class="start_game">
        <v-btn @click="startGame">开始游戏</v-btn>
      </div>
    </div>
  </div>
  <Footer />
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useTheme } from "vuetify";

const doubleThree = ref(true);
const doubleFour = ref(true);
const longConnect = ref(true);

// 图片 import
import logoWhite from "@/assets/image/logo_white.png";
import logoBlack from "@/assets/image/logo_black.png";

const items = [
  { title: "", disabled: false, href: "/" },
  { title: "游戏", disabled: false, href: "/" },
  { title: "双人对弈", disabled: false, href: "/game/pvp" },
];

const diffs = ref("medium");

import { useRouter } from "vue-router";
const router = useRouter();

const startGame = () => {
  router.push({
    path: "/game/pvp/play",
    query: {
      doubleThree: doubleThree.value,
      doubleFour: doubleFour.value,
      longConnect: longConnect.value,
    },
  });
};

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
  title: "双人对弈 - 棋局设置 - Gobang OL",
  meta: [
    { name: "description", content: "Gobang OL 双人对弈（PVP）- 棋局设置" },
  ],
});
</script>

<style scoped>
.site-logo {
  height: 15px;
}

/* 浅色模式 logo 放大 15%
.site-logo.dark {
  transform: scale(1.15);
  transform-origin: left center;
} */

.container {
  height: 100px;
}

.setting {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 80%;
}

.setting-item {
  margin-top: 20px;
  margin-bottom: 20px;
  background-color: #8a8a8a1a;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-top: 15px;
  padding-bottom: 0px;
  border-radius: 10px;
}

.setting-item-content {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}

.setting-item-title {
  margin-bottom: 10px;
}

.setting-item-content * {
  margin: -2px 5px;
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

.link {
  margin-bottom: 20px;
}

.start_game {
  flex: 1;
}

::v-deep(.setting a:link) {
  color: #0b9dff !important;
}

::v-deep(.setting a),
::v-deep(.setting a:visited),
::v-deep(.setting a:active) {
  color: #0b9dff !important;
  text-decoration: none !important;
  display: inline-block;
  padding: 4px 6px; /* 固定 padding */
  border-radius: 5px;
  transition: transform 0.3s cubic-bezier(0, -0.55, 0.42, 1.55),
    background-color 0.2s cubic-bezier(0, -0.55, 0.27, 1.55);
}

::v-deep(.setting a:hover) {
  color: rgb(255, 192, 192) !important;
  background-color: #cccccc3f;
  transform: scale(1.3); /* 整体放大 30% */
}
</style>
