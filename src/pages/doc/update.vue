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
v0.1.0   | 2025-08-18 | 继续完善基础功能
              </pre>
              <h2>提交日志（页面更新可能延迟）</h2>
              <a
                href="https://github.com/YuleBest/gobangol/commits/main"
                target="_blank"
                >最新日志请到 GitHub 查看</a
              >
              <pre>
Authon   | Date       | Commit
---------|------------|----------------------------------------------------------
YuleBest | 2025-08-18 | feat(game/pvp), fix(router). style(index, ui). refactor(ui): 添加双人对弈高级设置页面并优化游戏体验
YuleBest | 2025-08-18 | feat(router): 添加404页面及路由配置
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
YuleBest | 2025-08-17 | feat(doc): 添加文档页面和更新日志文档
YuleBest | 2025-08-17 | [test}ci(git): 利用git hooks在git commit执行之前自动更新public/update_log,txt
YuleBest | 2025-08-17 | style(ui), fix(game/pve): 优化游戏页面布局并优化PVE功能
YuleBest | 2025-08-16 | feat:(game/pve): 优化棋子绘制逻辑
YuleBest | 2025-08-16 | feat(game/pve): 添加评分显示功能并调整游戏界面样式
YuleBest | 2025-08-16 | chore: 添加腾讯验证文件
YuleBest | 2025-08-16 | style(game/pve,ui): 更新人机对弈页面logo和主题适配
YuleBest | 2025-08-16 | feat(ui): 添加深色/浅色主题切换功能
YuleBest | 2025-08-16 | style(logo,icon): 更新网站图标和logo，支持深色模式
YuleBest | 2025-08-16 | feat(game/pvp): 添加对局ID生成功能并调整样式
YuleBest | 2025-08-16 | feat(game/pve): 添加噩梦模式并实现难度相关AI逻辑
YuleBest | 2025-08-16 | style: 优化样式和提示文本
YuleBest | 2025-08-16 | style(ui): 调整游戏界面布局和样式
YuleBest | 2025-08-16 | feat(router): 重构游戏页面路由结构并添加难度选择
YuleBest | 2025-08-16 | refactor(Footer): 移除未使用的社交媒体图标代码
YuleBest | 2025-08-16 | style(ui/GameBody): 统一游戏界面中的步数显示和玩家提示
YuleBest | 2025-08-16 | feat(GameBodyPVP,GameBodyPVE): 重构游戏组件结构并添加音效
YuleBest | 2025-08-15 | feat(pve): 实现人机对战功能并更新版本至v0.0.3
YuleBest | 2025-08-15 | refactor(GameBody): 使用TypeScript重构五子棋组件代码
YuleBest | 2025-08-15 | fix(GameBody): 修复胜利判断bug，优化棋子动画和胜利状态处理
YuleBest | 2025-08-15 | chore(GameBody): 统一字符串引号格式并优化代码格式
YuleBest | 2025-08-15 | feat(GameBody): 添加棋子放置确认机制和预览功能
YuleBest | 2025-08-15 | feat(GameBody): 添加步数显示和游戏结束弹窗
YuleBest | 2025-08-15 | feat(GameBody): 添加胜利线绘制功能并优化胜利检测
YuleBest | 2025-08-15 | feat(GameBody): 为最后落子添加红色描边效果
YuleBest | 2025-08-15 | feat(GameBody): 为围棋棋盘添加星位
YuleBest | 2025-08-15 | feat(game/pvp): 添加返回首页按钮并调整游戏区域最大宽度
YuleBest | 2025-08-15 | chore: 更新版本号至0.0.2并完善README文档
YuleBest | 2025-08-15 | feat(game): 实现五子棋游戏核心功能与界面
YuleBest | 2025-08-15 | chore(ui): 删除了一些不打算上线的内容
YuleBest | 2025-08-15 | feat(ui): frist commit
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
