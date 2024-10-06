import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import router from './router'; // 引入路由
import axios from 'axios';

axios.defaults.baseURL = 'http://127.0.0.1:5000'; // Flask 伺服器的網址
// 創建應用並掛載路由
createApp(App).use(router).mount('#app');
