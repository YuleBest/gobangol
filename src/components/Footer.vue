<template>
  <v-divider :thickness="2"></v-divider>
  <v-footer class="text-center d-flex flex-column ga-2 py-4">
    <!-- <div class="d-flex ga-3">
      <v-btn
        v-for="icon in icons"
        :key="icon"
        :icon="icon"
        density="comfortable"
        variant="text"
      ></v-btn>
    </div> -->

    <div>{{ new Date().getFullYear() }} — <strong>于乐Yule</strong></div>
  </v-footer>
</template>

<script setup>
// const icons = ["mdi-facebook", "mdi-twitter", "mdi-linkedin", "mdi-instagram"];
</script>

<style scoped></style>
