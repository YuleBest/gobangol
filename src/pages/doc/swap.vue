<template>
  <Topbar />
  <div class="doc">
    <mdDoc />
  </div>
  <Footer />
</template>

<script lang="ts" setup>
import mdDoc from "@/assets/doc/swap.md";
import { useHead } from "@vueuse/head";
useHead({
  title: "交换规则 - Gobang OL 文档",
  meta: [{ name: "description", content: "五子棋交换规则" }],
});
</script>

<style>
@import "@/assets/style/doc.css";
</style>
