<template>
  <div class="topbar">
    <v-app-bar :elevation="0" color="transparent" height="60">
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
      <template v-slot:append>
        <v-btn icon="mdi-home" to="/"></v-btn>
        <v-btn icon="mdi-cog" to="/setting"></v-btn>
        <v-btn icon="mdi-book" to="/doc"></v-btn>
        <!-- 主题切换下拉 -->
        <v-menu>
          <template v-slot:activator="{ props }">
            <v-btn v-bind="props" icon>
              <v-icon>mdi-theme-light-dark</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item @click="setTheme('light')">
              <v-list-item-title>浅色模式</v-list-item-title>
            </v-list-item>
            <v-list-item @click="setTheme('dark')">
              <v-list-item-title>深色模式</v-list-item-title>
            </v-list-item>
            <v-list-item @click="setTheme('system')">
              <v-list-item-title>跟随系统</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </template>
    </v-app-bar>
  </div>
</template>

<style scoped>
.v-toolbar {
  position: relative; /* 为伪元素定位 */
  z-index: 1; /* 确保文字在上层 */
}

.v-toolbar::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: transparent; /* 不改变颜色 */
  backdrop-filter: blur(50px); /* 模糊背景 */
  -webkit-backdrop-filter: blur(50px); /* Safari 支持 */
  z-index: -1; /* 放在文字下面 */
}
</style>

<script setup>
import { onMounted, ref, watch } from "vue";
import { useTheme } from "vuetify";

// **模块导入 logo**
import logoWhite from "@/assets/image/logo_white.png";
import logoBlack from "@/assets/image/logo_black.png";

const theme = useTheme();

// 初始化主题
onMounted(() => {
  const saved = localStorage.getItem("themeMode");
  if (saved === "light" || saved === "dark" || saved === "system") {
    theme.change(saved);
  }
});

// 切换主题
function setTheme(mode) {
  theme.change(mode);
  localStorage.setItem("themeMode", mode);
}

// 是否为深色模式
const isDarkMode = ref(theme.global.current.value.dark);

// 监听 theme 变化（包括系统模式）
watch(
  () => theme.global.current.value,
  (val) => {
    isDarkMode.value = val.dark;
  },
  { deep: true, immediate: true }
);
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

.logo {
  padding-left: 20px;
}
</style>
