<template>
  <Topbar />
  <div class="doc">
    <mdDoc />
  </div>
  <Footer />
</template>

<script lang="ts" setup>
import mdDoc from "@/assets/doc/gomoku.md";
import { useHead } from "@vueuse/head";
useHead({
  title: "关于五子棋 - Gobang OL 文档",

  meta: [{ name: "description", content: "关于五子棋" }],
});
</script>

<style>
@import "@/assets/style/doc.css";
</style>
