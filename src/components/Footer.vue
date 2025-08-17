<template>
  <v-divider :thickness="2"></v-divider>
  <v-footer class="text-center d-flex flex-column ga-2 py-4">
    <div>本站已被访问过 <span id="busuanzi_site_pv"></span> 次</div>
    <div class="medal">
      <!-- Vue 勋章 -->
      <a href="https://vuejs.org" title="Vue 勋章" target="_blank">
        <img :src="vueBadge" style="height: 40px" />
      </a>
      <!-- TypeScript 勋章 -->
      <a
        href="https://www.typescriptlang.org"
        title="TypeScript 勋章"
        target="_blank"
      >
        <img :src="tsBadge" style="height: 40px" />
      </a>
      <!-- GitHub 勋章 -->
      <a
        href="https://github.com/YuleBest/gobangol"
        title="GitHub 勋章"
        target="_blank"
      >
        <img :src="githubBadge" style="height: 40px" />
      </a>
      <!-- Trust SSL 安全签章 -->
      <a
        class="trustssl"
        href="https://www.trustssl.cc/trust.php?sn=Z29iYW5nLmxoNTIwLnB3"
        title="Trust SSL安全认证签章"
        target="_blank"
      >
        <img
          src="https://static.coolcdn.cn/images/TrustSSL.png"
          style="height: 25px"
        />
      </a>
    </div>
    <div>
      Copyright &copy; {{ new Date().getFullYear() }}
      <strong
        ><a href="https://github.com/YuleBest" target="_blank"
          >于乐Yule</a
        ></strong
      >
      All right reserved.
    </div>

    <div class="end">
      <!-- 版权信息© -->
      <div>
        <a href="/doc/copyright" title="版权信息©" target="_self"> 版权信息</a>
      </div>
      <!-- 关于本站（about页面待开发） -->
      <div>
        <a href="/about" title="关于本站" target="_self"> 关于本站</a>
      </div>
      <!-- Urlquery 安全检测报告 -->
      <div>
        <a
          href="https://www.urlquery.net/report/fa232734-b0fd-4b2a-acd7-4a19aad5a18f"
          title="Urlquery安全检测报告"
          target="_blank"
        >
          Urlquery报告</a
        >
      </div>
    </div>
  </v-footer>
</template>

<script setup lang="ts">
import vueBadge from "@/assets/image/Vue.png";
import tsBadge from "@/assets/image/TypeScript.png";
import githubBadge from "@/assets/image/GitHub.png";
</script>

<style scoped>
.medal {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}

.medal *:not(.trustssl) {
  margin: 0 -2px;
}

.medal .trustssl {
  margin: 0 4px;
}

::v-deep(a),
::v-deep(a:link),
::v-deep(a:visited),
::v-deep(a:active) {
  color: var(--link-color) !important;
  text-decoration: none !important;
  display: inline-block;
  padding: 4px 6px; /* 固定 padding */
  border-radius: 5px;
  transition: transform 0.3s cubic-bezier(0, -0.55, 0.42, 1.55),
    background-color 0.2s cubic-bezier(0, -0.55, 0.27, 1.55);
}

::v-deep(a:hover) {
  color: rgb(255, 192, 192) !important;
  background-color: #cccccc3f;
  transform: scale(1.3); /* 整体放大 30% */
}

.end {
  display: flex;
}

.end * {
  margin: 0 3px;
}
</style>
