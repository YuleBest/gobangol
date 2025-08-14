<template>
  <div class="chat">
    <v-text-field
      label="消息"
      prepend-icon="mdi-message"
      append-icon="mdi-send"
      variant="outlined"
    ></v-text-field>
  </div>
</template>

<style scoped>
.chat {
  padding: 10px 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>

<script setup></script>
