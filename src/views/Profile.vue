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

<style scoped>
.profile-container {
  max-width: 500px; 
  margin: 0 auto; 
  padding: 20px; 
  background-color: #4b2d2dfd; 
  border-radius: 20px; /* 邊框圓角 */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center; /* 標題置中 */
  color: #fff9f2; /* 標題顏色 */
}

.profile-form {
  display: flex; /* 使用彈性布局 */
  flex-direction: column; /* 直列方向 */
}

.form-group {
  margin-bottom: 15px;
  color: #ffffff;
}

label {
  margin-bottom: 5px; 
}

input {
  padding: 10px; 
  border: 1px solid #ccc; 
  border-radius: 4px; 
  width: 100%; 
  box-sizing: border-box; 
}

.save-button {
  padding: 10px; 
  background-color: #28a745; 
  color: white;
  border: none; 
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s; 
}

.save-button:hover {
  background-color: #218838; 
}

.back-link {
  display: inline-block;
  margin-top: 20px; 
  text-align: center;  
  color: #007bff; 
  text-decoration: none; 
}

.back-link:hover {
  text-decoration: underline; 
}
</style>
