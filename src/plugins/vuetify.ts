/**
 * plugins/vuetify.ts
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";
import { VStepperVertical } from "vuetify/labs/VStepperVertical";
import { md3 } from "vuetify/blueprints";

// Composables
import { createVuetify } from "vuetify";

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    defaultTheme: "system",
  },
  components: {
    VStepperVertical,
  },
  blueprint: md3,
});
