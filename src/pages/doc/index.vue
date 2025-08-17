<template>
  <Topbar />
  <div class="main">
    <div class="title">
      <h1>文档</h1>
      <p>这里包含了 GoBang OL 的相关文档</p>
    </div>
    <v-divider :thickness="2"></v-divider>
    <div class="doc-list">
      <v-card class="mx-auto" max-width="300">
        <v-list :items="items"></v-list>
      </v-card>
    </div>
  </div>
</template>

<script setup>
const items = [
  {
    title: "更新日志",
    value: 1,
    props: {
      to: "/doc/update",
    },
  },
];
</script>

<style scoped>
.main {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  width: 100%;
}

.title {
  margin: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.title h1 {
  font-size: 36px;
}

.title p {
  font-size: 14px;
  color: #666;
}
</style>
