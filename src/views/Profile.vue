<template>
  <div class="profile-container">
    <h1>會員資料</h1>
    <form @submit.prevent="handleSave" class="profile-form">
      <div class="form-group">
        <label for="name">姓名:</label>
        <input type="text" id="name" v-model="user.name" />
      </div>
      <div class="form-group">
        <label for="email">電子郵件:</label>
        <input type="email" id="email" v-model="user.email" />
      </div>
      <div class="form-group">
        <label for="address">外送地址:</label>
        <input type="text" id="address" v-model="user.address" />
      </div>
      <div class="form-group">
        <label for="phone">電話:</label>
        <input type="tel" id="phone" v-model="user.phone" />
      </div>
      <button type="submit" class="save-button">保存</button>
    </form>
    <router-link to="/" class="back-link">返回</router-link>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
  setup() {
    const user = ref({
      name: '',
      email: '',
      address: '',
      phone: ''
    });

    const getUserData = () => {
      // 從 localStorage 獲取用戶資料
      const storedUser = JSON.parse(localStorage.getItem('user')) || {};
      user.value = { ...user.value, ...storedUser }; // 將存儲的資料合併到 user 物件
    };

    const handleSave = () => {
      // 保存用戶資料到 localStorage
      localStorage.setItem('user', JSON.stringify(user.value));
      alert('資料已保存！');
    };

    onMounted(() => {
      getUserData();
    });

    return {
      user,
      handleSave
    };
  }
};
</script>

<style>
.profile-container {
  max-width: 500px;
  margin: 0 auto;
  padding: 30px;
  background: linear-gradient(135deg, #45cca8, #68ff46); 
  border-radius: 20px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); 
}

h1 {
  text-align: center;
  color: #fff;
  font-size: 2.2rem;
  margin-bottom: 30px;
  font-weight: 700;
}

.profile-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 20px;
  color: #f1f1f1;
}

label {
  display: block;
  font-size: 1.1rem;
  margin-bottom: 5px;
  color: #fff; 
}

input {
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  width: 100%;
  box-sizing: border-box;
  background-color: #fff;
  font-size: 1rem;
  color: #333;
  transition: all 0.3s ease;
}

input:focus {
  border-color: #D2691E; 
  box-shadow: 0 0 8px rgba(210, 105, 30, 0.5); 
}

.save-button {
  padding: 12px;
  background-color: #f7e5e5; 
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.save-button:hover {
  background: linear-gradient(135deg, #45cca8, #2df600); 
  transform: translateY(-2px);
}

.save-button:active {
  transform: translateY(2px);
}

.back-link {
  display: inline-block;
  margin-top: 20px;
  text-align: center;
  color: #fff;
  font-size: 1.1rem;
  text-decoration: none;
  transition: color 0.3s;
}

.back-link:hover {
  text-decoration: underline;
  color: #D2691E; /* 懸停時文字顏色改為暖橙色 */
}
</style>