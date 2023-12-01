import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import VNetworkGraph from "v-network-graph";

import "v-network-graph/lib/style.css";
import "bootstrap/dist/css/bootstrap.css";

const app = createApp(App);

app.use(router);
app.use(VNetworkGraph);

app.mount("#app");
