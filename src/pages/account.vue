<template>
  <Topbar />
  <v-divider></v-divider>
  <v-card>
    <v-layout>
      <v-navigation-drawer expand-on-hover permanent rail>
        <v-list>
          <v-list-item
            prepend-avatar="https://randomuser.me/api/portraits/women/85.jpg"
            title="Yule"
          ></v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-list density="compact" nav>
          <v-list-item
            prepend-icon="mdi-home"
            title="首页"
            value="home"
            to="/"
          ></v-list-item>

          <v-list-item
            prepend-icon="mdi-account"
            title="帐户"
            value="account"
            to="/account"
          ></v-list-item>

          <v-list-item
            prepend-icon="mdi-account-multiple"
            title="好友"
            value="friends"
            to="/friends"
          ></v-list-item>

          <v-list-item
            prepend-icon="mdi-clock"
            title="最近游戏"
            value="game"
            to="/game"
          ></v-list-item>
        </v-list>
      </v-navigation-drawer>

      <v-main
        style="
          height: calc(100vh - 61px);
          display: flex;
          flex-direction: column;
        "
      >
        <!-- 标题 -->
        <div class="title">
          <div class="title-icon">
            <v-icon>mdi-account</v-icon>
          </div>
          <h1>管理你的帐户</h1>
        </div>
      </v-main>
    </v-layout>
  </v-card>
  <Footer />
</template>

<style>
.title {
  display: flex;
  align-items: center;
  padding: 20px;
}

.title-icon {
  font-size: 25px;
}

.title h1 {
  font-size: 30px;
}
</style>

<script lang="ts" setup></script>
