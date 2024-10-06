import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import router from './router'; // 引入路由

// 創建應用並掛載路由
createApp(App).use(router).mount('#app');
