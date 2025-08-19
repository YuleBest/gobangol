<template>
  <div class="main">
    <div class="container">
      <v-breadcrumbs :items="items">
        <template v-slot:prepend>
          <div class="logo">
            <a href="/">
              <img
                class="site-logo"
                :src="isDarkMode ? logoWhite : logoBlack"
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
        <div
          class="setting-item"
          v-for="group in settingGroups"
          :key="group.title"
        >
          <div class="setting-item-title">
            <h3>{{ group.title }}</h3>
          </div>
          <div class="setting-item-content">
            <v-switch
              v-for="option in group.options"
              :key="option.label"
              :model-value="option.model.value"
              @update:modelValue="(newValue) => (option.model.value = newValue)"
              :label="option.label"
              inset
              color="primary"
            />
          </div>
        </div>
      </div>

      <a class="link" href="/doc/" target="_self"> 了解五子棋规则 </a>

      <div class="start_game">
        <v-btn @click="startGame" size="x-large">开始游戏</v-btn>
      </div>
    </div>
  </div>
  <Footer />
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useTheme } from "vuetify";
import { useRouter } from "vue-router";
import { useHead } from "@vueuse/head";

const router = useRouter();
const theme = useTheme();

const doubleThree = ref(true);
const doubleFour = ref(true);
const longConnect = ref(true);
const Swap2 = ref(false);
const allowUndo = ref(false);

import logoWhite from "@/assets/image/logo_white.png";
import logoBlack from "@/assets/image/logo_black.png";

const items = [
  { title: "", disabled: false, href: "/" },
  { title: "游戏", disabled: false, href: "/" },
  { title: "双人对弈", disabled: false, href: "/game/pvp" },
];

const settingGroups = [
  {
    title: "禁手设置",
    options: [
      { label: "三三禁手", model: doubleThree },
      { label: "四四禁手", model: doubleFour },
      { label: "长连禁手", model: longConnect },
    ],
  },
  {
    title: "交换设置",
    options: [{ label: "Swap2", model: Swap2 }],
  },
  {
    title: "游戏功能",
    options: [{ label: "允许悔棋", model: allowUndo }],
  },
];

const startGame = () => {
  router.push({
    path: "/game/pvp/play",
    query: {
      doubleThree: doubleThree.value,
      doubleFour: doubleFour.value,
      longConnect: longConnect.value,
      swap2: Swap2.value,
      allowUndo: allowUndo.value,
    },
  });
};

onMounted(() => {
  const saved = localStorage.getItem("themeMode");
  if (["light", "dark", "system"].includes(saved)) {
    theme.change(saved);
  }
});

const isDarkMode = computed(() => theme.global.current.value.dark);

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

.container {
  height: 100px;
}

.setting {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  padding: 20px;
  gap: 10px;
}

.setting-item {
  margin: 20px 0;
  padding: 15px 0;
  border-radius: 10px;
  background-color: #8a8a8a1a;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.setting-item * {
  margin: 0px 2px;
  align-items: center;
}

.setting-item-content {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.setting-item-title {
  margin-bottom: 10px;
}

.main {
  width: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.link {
  margin-bottom: 20px;
  color: #0b9dff !important;
  text-decoration: none !important;
  padding: 4px 6px;
  border-radius: 5px;
  transition: transform 0.3s cubic-bezier(0, -0.55, 0.42, 1.55),
    background-color 0.2s cubic-bezier(0, -0.55, 0.27, 1.55);
}

.link:hover {
  color: rgb(255, 192, 192) !important;
  background-color: #cccccc3f;
  transform: scale(1.3);
}

.start_game {
  margin-top: 20px;
}
</style>
