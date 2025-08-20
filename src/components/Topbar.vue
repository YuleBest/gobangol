<template>
  <div class="topbar">
    <v-app-bar :elevation="0" color="transparent" height="60">
      <!-- 小屏：汉堡菜单按钮 -->
      <v-app-bar-nav-icon v-if="isSmallScreen" @click.stop="drawer = !drawer" />

      <!-- LOGO 永远在左侧 -->
      <div class="logo">
        <a href="/">
          <img
            v-show="isDarkMode"
            class="site-logo light"
            :src="logoWhite"
            alt="logo"
          />
          <img
            v-show="!isDarkMode"
            class="site-logo dark"
            :src="logoBlack"
            alt="logo"
          />
        </a>
      </div>

      <!-- 推到右侧 -->
      <v-spacer />

      <!-- 右侧区域：导航 + 头像 -->
      <template v-slot:append>
        <div class="d-flex align-center" id="option">
          <!-- 大屏导航按钮 -->
          <div v-if="!isSmallScreen" class="d-flex align-center">
            <v-btn text="首页" to="/" class="text-btn"></v-btn>
            <v-btn text="设置" to="/setting" class="text-btn"></v-btn>
            <v-btn text="文档" to="/doc" class="text-btn"></v-btn>
            <v-menu>
              <template v-slot:activator="{ props }">
                <v-btn v-bind="props" class="text-btn"> 主题 </v-btn>
              </template>
              <v-list>
                <v-list-item @click="setTheme('light')"
                  ><v-list-item-title>浅色模式</v-list-item-title></v-list-item
                >
                <v-list-item @click="setTheme('dark')"
                  ><v-list-item-title>深色模式</v-list-item-title></v-list-item
                >
                <v-list-item @click="setTheme('system')"
                  ><v-list-item-title>跟随系统</v-list-item-title></v-list-item
                >
              </v-list>
            </v-menu>
          </div>

          <!-- 账户系统待完善 -->
          <!-- 右侧头像
          <v-avatar size="32" class="ml-3">
            <img :src="avatar" alt="User Avatar" />
          </v-avatar> -->
        </div>
      </template>
    </v-app-bar>

    <!-- 小屏抽屉菜单 -->
    <v-navigation-drawer v-model="drawer" location="left" temporary>
      <v-list>
        <v-list-item to="/" title="首页"></v-list-item>
        <v-list-item to="/setting" title="设置"></v-list-item>
        <v-list-item to="/doc" title="文档"></v-list-item>
        <v-divider></v-divider>
        <br />
        <p style="margin-left: 16px; font-size: 13px">主题设置</p>
        <v-list-item @click="setTheme('light')" title="浅色模式"></v-list-item>
        <v-list-item @click="setTheme('dark')" title="深色模式"></v-list-item>
        <v-list-item @click="setTheme('system')" title="跟随系统"></v-list-item>
      </v-list>
    </v-navigation-drawer>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from "vue";
import { useTheme, useDisplay } from "vuetify";
import logoWhite from "@/assets/image/logo_white.png";
import logoBlack from "@/assets/image/logo_black.png";
// import avatar from "@/assets/image/avatar.png";

const theme = useTheme();
``;
const { width } = useDisplay();
const drawer = ref(false);

onMounted(() => {
  const saved = localStorage.getItem("themeMode");
  if (saved === "light" || saved === "dark" || saved === "system") {
    theme.change(saved);
  }
});

function setTheme(mode) {
  theme.change(mode);
  localStorage.setItem("themeMode", mode);
}

const isDarkMode = ref(theme.global.current.value.dark);
watch(
  () => theme.global.current.value,
  (val) => {
    isDarkMode.value = val.dark;
  },
  { deep: true, immediate: true }
);

const isSmallScreen = computed(() => width.value < 960);
</script>

<style scoped>
.v-btn {
  font-family: "Mona Sans", Arial, sans-serif !important;
  font-weight: 400 !important;
}

.v-toolbar {
  position: relative;
  z-index: 1;
  padding-right: 10px;
}

.v-navigation-drawer {
  background-color: var(--footer-bg-color);
  backdrop-filter: blur(50px);
}

.v-toolbar::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: transparent;
  backdrop-filter: blur(50px);
  -webkit-backdrop-filter: blur(50px);
  z-index: -1;
}

#option {
  padding-right: 20px;
}

.site-logo {
  height: 20px;
  margin-top: 5px;
}

/* .site-logo.dark {
  transform: scale(1.15);
  transform-origin: left center;
} */

.logo {
  padding-left: 20px;
}

.text-btn {
  margin: 0 8px;
  font-family: "Microsoft YaHei", sans-serif;
}
</style>
