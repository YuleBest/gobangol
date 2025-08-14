<template>
  <Topbar />
  <v-divider></v-divider>
  <v-card>
    <v-layout>
      <v-main style="height: calc(100vh - 61px); display: flex; flex-direction: column;">
        <!-- 游戏菜单 -->
        <div class="game-menu">
          <h1>开始游戏</h1>
          <div class="game-menu-item">
            <v-btn prepend-icon="mdi-robot-happy" to="/game/pve" stacked> 人机对弈 </v-btn>
            <v-btn prepend-icon="mdi-account-multiple" to="/game/pvp" stacked>
              双人对弈
            </v-btn>
            <v-btn prepend-icon="mdi-web" to="/game/ol" stacked> 联机对弈 </v-btn>
          </div>
        </div>
        <!-- banner -->
        <div class="banner">
          <v-divider></v-divider>
          <br></br>
          <v-banner
            text="五子棋起源于中国，是全国智力运动会竞技项目之一，是一种两人对弈的纯策略型棋类游戏。又称连五子、五子连、串珠、五目、五目碰或五格等。玩家双方分别使用黑白两色的棋子，下在棋盘直线与横线的交叉点上，先形成五子连珠者获胜。"
            stacked
          >
            <template v-slot:actions>
              <v-btn
                href="https://baike.baidu.com/item/%E4%BA%94%E5%AD%90%E6%A3%8B/130266"
                target="_blank"
                >了解更多↗
              </v-btn>
            </template>
          </v-banner>
        </div>
      </v-main>
    </v-layout>
  </v-card>
  <Footer />
</template>

<style>
.game-menu {
  width: 100%;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 20px;
}

.game-menu h1 {
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 20px;
}

.game-menu-item button {
  margin: auto;
  margin: 10px;
}

.banner {
  width: 100%;
}
</style>

<script lang="ts" setup></script>
