<template>
  <v-divider :thickness="2"></v-divider>
  <v-footer class="text-center d-flex flex-column ga-2 py-4">
    <div>本站已被访问过 <span id="busuanzi_site_pv"></span> 次</div>
    <div>{{ new Date().getFullYear() }} — <strong>于乐Yule</strong></div>
  </v-footer>
</template>

<script setup>
// 这里不需要特别的逻辑
</script>

<style scoped></style>
