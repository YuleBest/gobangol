<template>
  <Topbar />
  <div class="main">
    <div class="welcome-section">
      <h1 class="welcome-title">Discover the</h1>
      <h1 class="welcome-title">Magic of Gobang</h1>
      <p class="welcome-subtitle">
        放松心情，开启五子棋之旅！与好友或对手轻松对弈，Gobang OL
        让每一步都充满乐趣！
      </p>
    </div>

    <div class="game-section">
      <v-container fluid class="px-0">
        <v-row>
          <v-col
            cols="12"
            sm="6"
            md="6"
            lg="3"
            v-for="card in gameCards"
            :key="card.title"
          >
            <v-card class="game-card" :to="card.to" hover elevation="4">
              <v-card-item>
                <v-icon size="48" class="mb-3">
                  {{ card.icon }}
                </v-icon>
                <v-card-title>{{ card.title }}</v-card-title>
                <v-card-text>{{ card.text }}</v-card-text>
              </v-card-item>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </div>
  <Footer />
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { useTheme } from "vuetify";
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
.main {
  margin: 0 40px 40px 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.welcome-section {
  height: 50vh;
  width: 80vw;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: left;
  align-self: flex-start;
}

.welcome-section h1 {
  font-stretch: expanded;
  line-height: 1.2;
  font-size: 50px;
}

.welcome-section p {
  padding-top: 8px;
  font-size: 16px;
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

.about-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.tips-section .v-card {
  border: 2px solid rgba(192, 240, 255, 0.144);
}

@media (max-width: 768px) {
  .welcome-section {
    padding: 20px;
    height: 40vh;
    width: 80vw;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .welcome-section h1 {
    font-stretch: expanded;
    line-height: 1.2;
    font-size: 32px;
    text-align: center;
  }

  .welcome-section p {
    padding-top: 8px;
    font-size: 14px;
    word-wrap: break-word;
    text-align: center;
  }
}
</style>
