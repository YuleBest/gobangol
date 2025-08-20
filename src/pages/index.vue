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
            <div class="game-card" @click="goTo(card.to)">
              <!-- 原内容 -->
              <div class="card-content">
                <div class="icon-and-title">
                  <v-icon :icon="card.icon" class="icon"></v-icon>
                  <h3 class="title">{{ card.title }}</h3>
                </div>
                <div class="text-and-content">
                  <p class="text">{{ card.text }}</p>
                </div>
              </div>

              <!-- 鼠标悬停提示 -->
              <div class="hover-play">Play now &gt;</div>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </div>
  <Footer />
</template>

<script setup lang="ts">
import router from "@/router";
import { ref, onMounted, watch } from "vue";
import { useTheme } from "vuetify";
const theme = useTheme();
const isDarkMode = ref(theme.global.current.value.dark);

onMounted(() => {
  const saved = localStorage.getItem("themeMode");
  if (saved) theme.change(saved);
});

function goTo(path: string) {
  router.push(path);
}

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
  min-height: calc(100vh - 60px);
}

.welcome-section {
  height: 50vh;
  width: 100vw;
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
  position: relative;
  border: 1.5px solid;
  border-radius: 10px;
  height: 100%;
  padding: 15px 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  user-select: none;
  transition: all 0.3s ease-in-out;
  overflow: hidden;
  background-color: var(--v-theme-surface);
  color: var(--v-theme-on-surface); /* 使用主题文字颜色 */
}

.game-card .card-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
  transition: opacity 0.3s ease-in-out;
}

.game-card:hover .card-content {
  opacity: 0;
}

.game-card .hover-play {
  position: absolute;
  top: 50%;
  left: -100%;
  transform: translateY(-50%);
  font-size: 20px;
  font-weight: bold;
  white-space: nowrap;
  transition: left 0.5s ease, color 0.3s ease;
  color: white;
}

.game-card:hover {
  background-color: #000;
  cursor: pointer;
}

.game-card .hover-play {
  position: absolute;
  top: 50%;
  left: -100%;
  transform: translateY(-50%);
  font-size: 20px;
  font-weight: bold;
  white-space: nowrap;
  transition: left 0.3s ease, transform 0.3s ease, opacity 0.3s ease;
  opacity: 0;
  color: white;
}

.game-card:hover .hover-play {
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 1;
}

.icon-and-title {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  gap: 10px;
}

.text-and-content {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  min-height: 0;
}

@media (max-width: 768px) {
  .main {
    margin: 0 20px 40px 20px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .welcome-section {
    padding: 20px;
    height: 40vh;
    width: 100vw;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    align-self: center;
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
