<template>
  <v-app>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
document.addEventListener("DOMContentLoaded", () => {
  const script = document.createElement("script");
  script.src = "//busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js";
  script.async = true;
  document.body.appendChild(script);
});
</script>

<style></style>
