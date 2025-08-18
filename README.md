# Gobang OL

> 一个现代化的在线五子棋对战平台，基于 Vue 3 + Vuetify 构建

## 🎮 项目概述

Gobang OL 是一个基于 Web 的在线五子棋对战游戏平台，采用现代化的前端技术栈开发，提供流畅的游戏体验和优雅的用户界面。项目支持实时对战、游戏记录、用户设置等功能，旨在为用户提供一个简洁而功能完善的在线五子棋游戏体验。

### ✨ 主要特性

- **现代化界面**：基于 Vuetify 3 的 Material Design 设计语言
- **响应式设计**：完美适配桌面端和移动端设备
- **实时对战**：支持在线匹配和好友对战
- **游戏记录**：保存和查看历史对局
- **个性化设置**：支持主题切换、音效控制等
- **TypeScript 支持**：完整的类型检查和开发体验

### 🛠️ 技术栈

- **前端框架**：Vue 3.5+ (Composition API)
- **UI 框架**：Vuetify 3 (Material Design)
- **路由管理**：Vue Router
- **构建工具**：Vite
- **开发语言**：TypeScript
- **样式预处理器**：Sass/SCSS
- **图标库**：Material Design Icons

## 🚀 开发进程

- [x] 项目基础架构（v0.0.1）
- [x] Vuetify 3 集成配置（v0.0.1）
- [x] 响应式布局实现（v0.0.1）
- [x] 基础游戏界面开发（v0.0.2）
- [x] 人机对战功能（v0.0.3）
- [ ] 联机游戏逻辑
- [ ] 用户系统
- [ ] 游戏记录
- [ ] MORE...

### 开发计划

- **Phase 1**: 基础游戏功能

  - 棋盘渲染和交互
  - 落子逻辑和胜负判定
  - 悔棋和重新开始功能

- **Phase 2**: 在线对战

  - WebSocket 连接
  - 匹配系统
  - 实时对战同步

- **Phase 3**: 用户系统

  - 用户注册和登录
  - 个人资料管理
  - 好友系统

- **Phase 4**: 高级功能
  - AI 对战模式
  - 观战系统
  - 排行榜和统计

## 🏗️ 本地部署

### 环境要求

- Node.js: 18.0.0 或更高版本
- npm: 9.0.0 或更高版本

### 快速开始

1. **克隆项目**

   ```bash
   git clone https://github.com/YuleBest/gobangol.git
   cd gobangol
   ```

2. **安装依赖**

   ```bash
   npm install
   ```

3. **启动开发服务器**

   ```bash
   npm run dev
   ```

4. **访问应用**
   打开浏览器访问: `http://localhost:7777`

### 构建命令

```bash
npm run build
```

### 项目结构

```tree
gobangol/
├── src/
│   ├── components/     # 可复用组件
│   ├── pages/          # 页面组件
│   ├── plugins/        # 插件配置
│   ├── router/         # 路由配置
│   ├── styles/         # 样式文件
│   └── assets/         # 静态资源
├── public/             # 公共资源
└── dist/               # 构建输出
```

## 🤝 贡献指南

欢迎贡献！如果您想为项目做出贡献，请遵循以下步骤：

1. Fork 本项目
2. 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 🙋‍♂️ 联系方式

如果您有任何问题或建议，请通过以下方式联系我们：

- 提交 [Issue](https://github.com/YuleBest/gobangol/issues)
- 发送邮件至: `yule-best@outlook.com`
