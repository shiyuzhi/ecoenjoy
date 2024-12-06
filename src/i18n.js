import { createI18n } from 'vue-i18n';

const i18n = createI18n({
  legacy: false,  // 使用 Composition API
  locale: 'zh',  // 預設語言
  messages: {
    en: {
      message: {
        hello: 'Hello, World!',
        login: 'Login',
        logout: 'Logout',
        restaurant: 'Restaurant',
      },
    },
    zh: {
      message: {
        hello: '你好，世界！',
        login: '登入',
        logout: '登出',
        restaurant: '餐廳',
      },
    },
  },
});

export default i18n;
