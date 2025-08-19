<template>
  <Topbar />
  <div class="doc">
    <mdDoc />
  </div>
  <Footer />
</template>

<script lang="ts" setup>
import mdDoc from "@/assets/doc/api.md";
</script>

<style>
@import "@/assets/style/doc.css";
</style>
