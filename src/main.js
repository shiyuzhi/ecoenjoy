import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import router from './router'; // 引入路由
import axios from 'axios';

axios.defaults.baseURL = 'http://127.0.0.1:5000'; // Flask 伺服器的網址

// 添加攔截器以自動在每個請求中添加 Authorization 標頭
axios.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('token'); // 假設 token 存儲在 localStorage 中
      if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );
  
// 創建應用並掛載路由
createApp(App).use(router).mount('#app');
