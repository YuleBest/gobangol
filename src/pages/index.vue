<template>
  <Topbar />
  <v-card class="fill-height">
    <v-layout>
      <v-main class="d-flex flex-column">
        <!-- 欢迎区域 -->
        <div
          class="welcome-section d-flex flex-column justify-center text-center text-white"
          :style="{
            backgroundImage: `url(${isDarkMode ? IndexBgBlack : IndexBgWhite})`,
          }"
        >
          <h1 class="welcome-title">欢迎来到 Gobang OL</h1>
          <p class="welcome-subtitle">享受对弈的乐趣吧</p>
        </div>

        <!-- 游戏模式选择 -->
        <div class="game-section">
          <v-container>
            <v-row>
              <v-col
                cols="12"
                md="6"
                lg="3"
                v-for="card in gameCards"
                :key="card.title"
              >
                <v-card class="game-card" :to="card.to" hover elevation="4">
                  <v-card-item>
                    <v-icon size="48" :color="card.color" class="mb-3">{{
                      card.icon
                    }}</v-icon>
                    <v-card-title>{{ card.title }}</v-card-title>
                    <v-card-text>{{ card.text }}</v-card-text>
                  </v-card-item>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
        </div>

        <!-- 游戏介绍 -->
        <div class="tips-section">
          <v-container>
            <v-card elevation="2" class="about-card">
              <v-card-title> 关于五子棋 </v-card-title>
              <v-card-text>
                五子棋起源于中国，是全国智力运动会竞技项目之一，是一种两人对弈的纯策略型棋类游戏。又称连五子、五子连、串珠、五目、五目碰或五格等。
              </v-card-text>
              <v-card-actions>
                <v-btn
                  href="https://baike.baidu.com/item/%E4%BA%94%E5%AD%90%E6%A3%8B/130266"
                  target="_blank"
                >
                  了解更多↗
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-container>
        </div>
      </v-main>
    </v-layout>
    <Footer />
  </v-card>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { useTheme } from "vuetify";
import IndexBgWhite from "@/assets/image/IndexBg_white.jpg";
import IndexBgBlack from "@/assets/image/IndexBg_black.png";

const theme = useTheme();
const isDarkMode = ref(theme.global.current.value.dark);

onMounted(() => {
  const saved = localStorage.getItem("themeMode");
  if (saved) theme.change(saved);
});

watch(
  () => theme.global.current.value.dark,
  (val) => (isDarkMode.value = val)
);

const gameCards = [
  {
    to: "/game/pve",
    icon: "mdi-robot-happy",
    color: "primary",
    title: "人机对弈",
    text: "与 AI 对战，从入门到精通，适合各个水平的玩家",
  },
  {
    to: "/game/pvp/play",
    icon: "mdi-account-multiple",
    color: "success",
    title: "双人对弈",
    text: "与朋友面对面切磋，体验真实的对弈乐趣",
  },
  {
    to: "/game/pvp",
    icon: "mdi-trophy",
    color: "warning",
    title: "双人对弈-高级设置",
    text: "专业对弈体验，支持禁手、Swap2，可禁用悔棋",
  },
  {
    to: "/game/ol",
    icon: "mdi-web",
    color: "info",
    title: "联机对弈（开发中）",
    text: "在线匹配全球玩家，与好友实时对战，体验竞技的刺激",
  },
];
</script>

<style scoped>
.welcome-section {
  padding: 20px;
  height: 80vh;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
  position: relative;
}
.welcome-section::before {
  content: "";
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
  z-index: 0;
}
.welcome-section::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 50px;
  background: linear-gradient(to bottom, transparent, #fff);
  z-index: 0;
}
.v-theme--dark .welcome-section::after {
  background: linear-gradient(to bottom, transparent, #212121);
  height: 100px;
}
.welcome-section > * {
  position: relative;
  z-index: 1;
}
.welcome-title {
  font-size: 42px;
  font-weight: 700;
  margin-bottom: 10px;
}
.welcome-subtitle {
  font-size: 20px;
}
.game-section {
  padding: 40px 20px;
}
.game-card {
  height: 100%;
  text-align: center;
  transition: all 0.3s ease;
  cursor: pointer;
  border: 2px solid rgba(255, 192, 203, 0.144);
}
.game-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15) !important;
}
.tips-section {
  padding: 0 20px 20px;
}
.about-card {
  height: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.tips-section .v-card {
  border: 2px solid rgba(192, 240, 255, 0.144);
}
@media (max-width: 768px) {
  .welcome-section {
    height: 50vh;
  }
  .welcome-title {
    font-size: 32px;
  }
  .welcome-subtitle {
    font-size: 16px;
  }
}
@media (max-width: 600px) {
  .welcome-title {
    font-size: 28px;
  }
  .welcome-section {
    padding: 20px 10px 10px;
  }
}
</style>
