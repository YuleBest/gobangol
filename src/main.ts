/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from "@/plugins";

// Components
import App from "./App.vue";

// Composables
import { createApp } from "vue";

// Pages Head
import { createHead } from "@vueuse/head";
const head = createHead();

// Styles
import "./assets/main.css";

const app = createApp(App);

registerPlugins(app);

app.mount("#app");
app.use(head);

head.push({
  title: "Gobang OL - 在线五子棋",
  meta: [
    {
      name: "description",
      content:
        "Gobang OL 是一个五子棋游戏网站，目前可以进行人机对弈和双人对弈的游玩，快来试试吧！",
    },
    {
      name: "keywords",
      content:
        "GobangOL, Gobang OL, 在线五子棋, 五子棋, 游戏, 好友对战, 人机对弈, 双人对弈, PVP, PVE, Gobang, gobang, Gobang Online, 在线五子棋游戏, 五子棋游戏, 在线对弈, 对弈, 五子棋对弈, 对弈游戏",
    },
  ],
});
