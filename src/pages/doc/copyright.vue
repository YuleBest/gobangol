<template>
  <Topbar />
  <div class="doc">
    <mdDoc />
  </div>

  <Footer />
</template>

<style>
@import "@/assets/style/doc.css";
</style>

<script>
import mdDoc from "@/assets/doc/copyright.md";
import { useHead } from "@vueuse/head";
useHead({
  title: "版权声明 & 开源许可 - Gobang OL 文档",

  meta: [{ name: "description", content: "Gobang OL 版权声明" }],
});
export default {
  components: {
    mdDoc, // 注意这里要和 template 中的名字一致
  },
};
</script>
