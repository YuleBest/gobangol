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
  script.src = "//api.busuanzi.cc/static/3.6.9/busuanzi.min.js";
  document.body.appendChild(script);
});
</script>

<style></style>
