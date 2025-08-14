<template style="weith: 100px">
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

      <v-main style="height: calc(100vh - 61px)">
        <router-view />
      </v-main>
    </v-layout>
  </v-card>
</template>

<script setup></script>
