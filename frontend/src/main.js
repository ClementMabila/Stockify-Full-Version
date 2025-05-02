import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css' 
import router from './router'
import App from './App.vue'
import { useAuthStore } from './store/auth'
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

const app = createApp(App)
app.config.globalProperties.$axios = axios;

app.use(createPinia())
app.use(router)

const authStore = useAuthStore()
authStore.setCsrfToken()

app.mount('#app')