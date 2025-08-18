<template>
  <Topbar />
  <v-divider></v-divider>
  <v-card class="fill-height">
    <v-layout>
      <v-main
        style="
          /* height: calc(100vh - 61px); */
          display: flex;
          flex-direction: column;
        "
      >
        <!-- 欢迎区域 -->
        <div
          class="welcome-section"
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
              <v-col cols="12" md="6" lg="3">
                <v-card class="game-card" to="/game/pve" hover elevation="4">
                  <v-card-item>
                    <v-icon size="48" color="primary" class="mb-3"
                      >mdi-robot-happy</v-icon
                    >
                    <v-card-title>人机对弈</v-card-title>
                    <v-card-text>
                      与AI对战，从入门到精通，适合各个水平的玩家
                    </v-card-text>
                  </v-card-item>
                </v-card>
              </v-col>

              <v-col cols="12" md="6" lg="3">
                <v-card
                  class="game-card"
                  to="/game/pvp/play"
                  hover
                  elevation="4"
                >
                  <v-card-item>
                    <v-icon size="48" color="success" class="mb-3"
                      >mdi-account-multiple</v-icon
                    >
                    <v-card-title>双人对弈</v-card-title>
                    <v-card-text>
                      与朋友面对面切磋，体验真实的对弈乐趣
                    </v-card-text>
                  </v-card-item>
                </v-card>
              </v-col>

              <v-col cols="12" md="6" lg="3">
                <v-card class="game-card" to="/game/pvp" hover elevation="4">
                  <v-card-item>
                    <v-icon size="48" color="warning" class="mb-3"
                      >mdi-trophy</v-icon
                    >
                    <v-card-title>双人对弈-高级设置</v-card-title>
                    <v-card-text> 专业对弈体验，支持禁手规则 </v-card-text>
                  </v-card-item>
                </v-card>
              </v-col>

              <v-col cols="12" md="6" lg="3">
                <v-card class="game-card" to="/game/ol" hover elevation="4">
                  <v-card-item>
                    <v-icon size="48" color="info" class="mb-3">mdi-web</v-icon>
                    <v-card-title>联机对弈（开发中）</v-card-title>
                    <v-card-text>
                      在线匹配全球玩家，与好友实时对战，体验竞技的刺激
                    </v-card-text>
                  </v-card-item>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
        </div>

        <!-- 游戏提示和介绍 -->
        <div class="tips-section">
          <v-container>
            <v-row>
              <v-col cols="12" md="6">
                <v-card elevation="2" class="tips-card">
                  <v-card-title> 游戏小贴士 </v-card-title>
                  <v-card-text>
                    <v-card-text> 先手黑棋，后手白棋 </v-card-text>
                    <v-card-text>
                      横、竖、斜任意方向连成五子即为胜利
                    </v-card-text>
                    <v-card-text>
                      高级设置支持禁手规则，增加游戏策略性
                    </v-card-text>
                    <v-card-text>
                      合理利用悔棋功能，学习和提高棋艺
                    </v-card-text>
                  </v-card-text>
                </v-card>
              </v-col>

              <v-col cols="12" md="6">
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
              </v-col>
            </v-row>
          </v-container>
        </div>
      </v-main>
    </v-layout>
    <Footer />
  </v-card>
</template>

<style scoped>
.welcome-section {
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 20px 20px 20px;
  height: 100vh;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
}

.welcome-section::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  z-index: 1;
}

.welcome-section::after {
  content: "";
  position: absolute;
  bottom: 0px;
  left: 0;
  right: 0;
  height: 50px;
  background: linear-gradient(to bottom, transparent, #ffffff);
  z-index: 1;
}

.theme--dark .welcome-section::after,
.v-theme--dark .welcome-section::after {
  background: linear-gradient(to bottom, transparent, rgb(33, 33, 33));
  height: 100px;
}

.welcome-section > * {
  position: relative;
  z-index: 2;
}

.game-section > * {
  position: relative;
  z-index: 2;
}

.welcome-title {
  font-size: 42px;
  font-weight: 700;
  margin-bottom: 10px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

.welcome-subtitle {
  font-size: 20px;
  margin-bottom: 0;
}

.game-section {
  padding: 40px 20px;
}

.game-card {
  height: 100%;
  text-align: center;
  transition: all 0.3s ease;
  cursor: pointer;
}

.game-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15) !important;
}

.game-card .v-card-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
}

.game-card .v-card-text {
  font-size: 14px;
  line-height: 1.6;
}

.tips-section {
  padding: 40px 20px;
}

.tips-card,
.about-card {
  height: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}

.about-card .v-card-title {
  font-size: 20px;
  font-weight: 600;
}

.game-section .v-card {
  border: 2px solid rgba(255, 192, 203, 0.144);
}

.tips-section .v-card {
  border: 2px solid rgba(192, 240, 255, 0.144);
}

@media (max-width: 768px) {
  .welcome-title {
    font-size: 32px;
  }

  .welcome-subtitle {
    font-size: 16px;
  }

  .welcome-section {
    height: 50vh;
  }
}

@media (max-width: 600px) {
  .welcome-section {
    padding: 20px 10px 10px;
  }

  .welcome-title {
    font-size: 28px;
  }

  .welcome-section {
    height: 50vh;
  }
}
</style>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from "vue";
import { useTheme } from "vuetify";

// 图片 import
import IndexBgWhite from "@/assets/image/IndexBg_white.jpg";
import IndexBgBlack from "@/assets/image/IndexBg_black.png";

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
  async (newVal, oldVal) => {
    isDarkMode.value = newVal.dark;
  },
  { deep: true, immediate: true }
);
</script>
