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
import axios from 'axios';

export default {
  setup() {
    const user = ref({
      name: '',
      email: '',
      address: '',
      phone: ''
    });

    const getUserData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/user'); // 獲取會員資料的API
        user.value = response.data;
      } catch (error) {
        console.error('獲取會員資料失敗:', error);
      }
    };

    const handleSave = async () => {
      try {
        await axios.put('http://127.0.0.1:5000/user', user.value); // 修改會員資料的API
        alert('資料已保存！');
      } catch (error) {
        console.error('保存失敗:', error);
      }
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
  background-color: #000000fd; 
  border-radius: 20px; /* 邊框圓角 */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center; /* 標題置中 */
  color: #ded2c4; /* 標題顏色 */
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
