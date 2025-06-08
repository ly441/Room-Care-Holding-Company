
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import axios from "axios";
import VueAxios from "vue-axios";


axios.defaults.baseURL = "http://localhost:8000/api";
axios.defaults.headers.common["Content-Type"] = "application/json";

// Axios response interceptor for global error handling (401)
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      store.commit("setToken", "");
      router.push("/login");
    }
    return Promise.reject(error);
  }
);

const app = createApp(App);

app.use(VueAxios, axios);
app.use(router);
app.use(store);

app.config.errorHandler = (err, vm, info) => {
  console.error("Global error handler:", err, info);
};

app.mount("#app");
