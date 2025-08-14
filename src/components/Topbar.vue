<template>
  <v-app-bar :elevation="0" height="60">
    <v-btn
      to="/"
      :style="{ ':active': { backgroundColor: '#00000000' }, fontSize: '16px' }"
    >
      五子棋在线
    </v-btn>
    <template v-slot:append>
      <v-btn icon="mdi-home" to="/"></v-btn>
      <v-btn icon="mdi-cog" to="/setting"></v-btn>
    </template>
  </v-app-bar>
</template>

<script setup></script>
