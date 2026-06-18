import { createApp } from "vue";
import { createPinia } from "pinia";
import axios from "axios";

import App from "./App.vue";
import router from "./router";
import { useUserStore } from '@/stores/user';

import "./assets/main.css";

// console.log('URL', import.meta.env.VITE_API_URL)
axios.defaults.baseURL = import.meta.env.VITE_API_URL;

const app = createApp(App);

const pinia = createPinia();
app.use(pinia);
app.use(router, axios);

const userStore = useUserStore(pinia);
userStore.router = router; // Pass router instance to store

app.mount("#app");