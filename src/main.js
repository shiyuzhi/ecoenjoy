import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import router from './router'; // 引入路由
import axios from 'axios';
import i18n from './i18n';

axios.defaults.baseURL = 'http://127.0.0.1:5000'; // Flask 伺服器的網址

// 添加攔截器以自動在每個請求中添加 Authorization 標頭
axios.interceptors.request.use(
  (config) => {
    const token = sessionStorage.getItem('token'); // 假設你將 token 存儲在 sessionStorage 中
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 創建應用並掛載路由，並註冊 i18n
createApp(App)
  .use(router)
  .use(i18n)  // 註冊 i18n
  .mount('#app');
