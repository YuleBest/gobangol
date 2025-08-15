<template>
  <div class="topbar">
    <v-app-bar :elevation="0" height="60">
      <div class="logo">
        <a href="/">
          <img class="site-logo light" src="/logo_white.png" alt="logo" />
          <img class="site-logo dark" src="/logo_black.png" alt="logo" />
        </a>
      </div>
      <template v-slot:append>
        <v-btn icon="mdi-home" to="/"></v-btn>
        <v-btn icon="mdi-cog" to="/setting"></v-btn>
      </template>
    </v-app-bar>
  </div>
</template>

<style scoped>
.site-logo {
  height: 15px;
}

.logo {
  padding-left: 20px;
}

/* 默认浅色模式显示白色 logo */
.light {
  display: inline;
}
.dark {
  display: none;
}

/* 深色模式显示黑色 logo */
@media (prefers-color-scheme: dark) {
  .light {
    display: none;
  }
  .dark {
    display: inline;
  }
}
</style>
