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
import mdDoc from "@/assets/doc/update.md";

export default {
  components: {
    mdDoc, // 注意这里要和 template 中的名字一致
  },
};
</script>
