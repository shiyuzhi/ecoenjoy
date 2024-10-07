<template>
  <div class="register-container">
    <h2 class="form-title">Register</h2>
    <form @submit.prevent="handleRegister" class="register-form">
      <div class="form-group">
        <label for="username">使用者名稱</label>
        <input type="text" v-model="username" id="username" required />
      </div>
      <div class="form-group">
        <label for="email">電子郵件</label>
        <input type="email" v-model="email" id="email" required />
      </div>
      <div class="form-group">
        <label for="password">密碼</label>
        <input type="password" v-model="password" id="password" required />
      </div>
      <div class="form-group">
        <label for="confirmPassword">確認密碼</label>
        <input type="password" v-model="confirmPassword" id="confirmPassword" required />
      </div>
      <button type="submit" class="submit-button">Register</button>
      <div class="auth-buttons">
        <button class="login-button" @click="toggleLoginModal">已有帳戶? 登入</button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';  // 確保安裝了axios

export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
    };
  },
  methods: {
    async handleRegister() {
      if (this.password !== this.confirmPassword) {
        alert("密碼不一致！");
        return;
      }

      // 可以加入正則表達式來檢查 email 格式
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailPattern.test(this.email)) {
        alert("請輸入有效的電子郵件地址！");
        return;
      }

      try {
        const response = await axios.post('http://localhost:5000/register', {
          username: this.username,
          email: this.email,
          password: this.password,
        });

        if (response.data.success) {
          alert(`註冊成功！用戶名: ${this.username}`);
          // 可以在這裡重定向到登入頁面
          this.toggleLoginModal();
        } else {
          alert('註冊失敗！請檢查您的資料。');
        }
      } catch (error) {
        console.error(error);
        alert('發生錯誤，請稍後再試。');
      }
    },
    toggleLoginModal() {
      // 切換到登入畫面
      this.$router.push('/login'); 
    }
  },
};
</script>

<style scoped>
.register-container {
  width: 350px; 
  margin: 50px auto; 
  background-color: #cfeed0; 
  border-radius: 12px; 
  padding: 30px; 
  box-shadow: 0 4px 15px rgba(52, 30, 30, 0.2); 
}

.form-title {
  text-align: center;
  color: #00796b; 
  margin-bottom: 20px;
}

.register-form {
  display: flex;
  flex-direction: column; 
}

.form-group {
  margin-bottom: 15px; 
}

.form-group label {
  display: block; 
  margin-bottom: 5px; 
  font-weight: bold; 
}

.form-group input {
  padding: 10px; 
  border: 1px solid #5b3a3a; 
  border-radius: 8px; 
  width: 100%; 
  box-sizing: border-box; 
}

.submit-button {
  padding: 12px; 
  background-color: #25a294; 
  color: white; 
  border: none; 
  border-radius: 4px; 
  cursor: pointer; 
  font-size: 1em; 
}

.submit-button:hover {
  background-color: #004d40; 
}

.auth-buttons {
  display: flex; 
  justify-content: center; 
  margin-top: 15px; 
}

.auth-buttons button {
  padding: 10px 15px; 
  border: none; 
  border-radius: 4px; 
  background-color: #4CAF50; 
  color: white; 
  cursor: pointer; 
  transition: background-color 0.3s; 
}

.auth-buttons button:hover {
  opacity: 0.9; 
}
</style>
