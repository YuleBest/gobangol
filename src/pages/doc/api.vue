<template>
  <Topbar />
  <div class="doc">
    <mdDoc />
  </div>
  <Footer />
</template>

<script lang="ts" setup>
import mdDoc from "@/assets/doc/api.md";
import { useHead } from "@vueuse/head";
useHead({
  title: "Gobang OL | 在线房间系统 API 文档 - Gobang OL 文档",

  meta: [{ name: "description", content: "Gobang OL 在线房间系统 API 文档" }],
});
</script>

<style>
@import "@/assets/style/doc.css";
</style>
