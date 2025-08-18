<template>
  <Topbar />
  <div class="main">
    <div class="tabs">
      <v-card>
        <v-tabs v-model="tab" align-tabs="center">
          <v-tab value="one">更新日志</v-tab>
        </v-tabs>

        <v-card-text>
          <v-tabs-window v-model="tab">
            <v-tabs-window-item value="one">
              <h2>版本日志</h2>
              <pre>
Version  | Date       | Description
---------|------------|----------------------------------------------------------
v0.0.5   | 2025-08-17 | 基本框架搭建
              </pre>
              <h2>提交日志（页面更新可能延迟）</h2>
              <a
                href="https://github.com/YuleBest/gobangol/commits/main"
                target="_blank"
                >最新完整日志请到 GitHub 查看</a
              >
              <pre>
Authon   | Date       | Commit
---------|------------|----------------------------------------------------------
YuleBest | 2025-08-18 | style(Footer): 调整页脚样式和字体大小
YuleBest | 2025-08-18 | style(Footer): 调整勋章尺寸并优化间距布局
YuleBest | 2025-08-18 | feat(Footer): 添加Urlquery安全检测报告链接
YuleBest | 2025-08-18 | fix: 修正构建脚本中错误的sitemap更新文件名
YuleBest | 2025-08-18 | style(game/pve): 调整站点logo高度为15px以优化显示效果  
YuleBest | 2025-08-18 | fix: 修复构建失败，修正图片路径
YuleBest | 2025-08-18 | chore(SEO): 添加搜索引擎验证文件
YuleBest | 2025-08-18 | feat(SEO), chore(data): 添加SEO优化，优化资源管理功能  
YuleBest | 2025-08-18 | chore(router): 代码风格统一化，统一使用双引号替换单引号
YuleBest | 2025-08-18 | feat: 添加版权页面和页脚勋章链接
YuleBest | 2025-08-18 | chore: 添加SSL域名验证文件用于信任验证
YuleBest | 2025-08-18 | feat: 添加不蒜子统计功能
YuleBest | 2025-08-17 | test: 增加部分为联机功能做铺垫的对接代码
Yule     | 2025-08-17 | style(doc): 优化移动端浏览更新日志的体验
Yule     | 2025-08-17 | style(doc): 缩小更新日志的字号
YuleBest | 2025-08-17 | style(ui), fix(game/pve): 优化游戏页面布局并优化PVE功能
...
              </pre>
            </v-tabs-window-item>
          </v-tabs-window>
        </v-card-text>
      </v-card>
    </div>
  </div>
  <Footer />
</template>

<script setup>
import { useHead } from "@vueuse/head";
import { ref } from "vue";

const tab = ref("one");

useHead({
  title: "更新日志 - Gobang OL",
  meta: [{ name: "description", content: "Gobang OL 更新日志" }],
});
</script>

<style scoped>
.main {
  display: flex;
  flex-direction: column;
  height: 100%;
  align-items: center;
}

.tabs {
  padding: 20px;
}

.tabs h2 {
  margin-bottom: 10px;
}

.tabs pre {
  font-size: 14px;
  max-width: 80vw;
  overflow-x: auto;
  white-space: pre;
}

.log-list {
  max-width: 50%;
}

::v-deep(.tabs a),
::v-deep(.tabs a:link),
::v-deep(.tabs a:visited),
::v-deep(.tabs a:active),
::v-deep(.tabs a:hover) {
  color: rgb(255, 192, 192) !important;
  text-decoration: none !important;
}
</style>
