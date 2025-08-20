/**
 * plugins/vuetify.ts
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";
import { VStepperVertical } from "vuetify/labs/VStepperVertical";
// import { md3 } from "vuetify/blueprints";

// Composables
import { createVuetify } from "vuetify";

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides

export default createVuetify({
  theme: {
    defaultTheme: "blackWhiteLight", // 默认使用浅色
    themes: {
      // 浅色主题
      blackWhiteLight: {
        dark: false,
        colors: {
          primary: "#000000", // 主色：黑
          secondary: "#ffffff", // 次色：白
          background: "#ffffff", // 背景
          surface: "#ffffff", // 卡片/组件表面
          success: "#000000",
          error: "#000000",
          info: "#000000",
          warning: "#000000",
        },
      },
      // 深色主题
      blackWhiteDark: {
        dark: true,
        colors: {
          primary: "#ffffff", // 主色：白
          secondary: "#000000", // 次色：黑
          background: "#000000", // 背景
          surface: "#111111", // 卡片/组件表面
          success: "#ffffff",
          error: "#ffffff",
          info: "#ffffff",
          warning: "#ffffff",
        },
      },
    },
  },
  // blueprint: md3,
  components: {
    VStepperVertical,
  },
});
