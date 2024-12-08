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
        // 檢查密碼是否一致
        if (this.password !== this.confirmPassword) {
          alert("密碼不一致！");
          return;
        }
  
        // 檢查 email 格式是否有效
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
  
          // 打印回應，方便調試
          console.log(response); // 確認回應格式
  
          // 根據回應決定註冊是否成功
          if (response.data.success) {
            alert(`註冊成功！用戶名: ${this.username}`);
            this.toggleLoginModal();  // 成功後跳轉到登入頁面
          } else {
            alert(`註冊失敗！${response.data.message}`);
          }
        } catch (error) {
          console.error(error); // 記錄錯誤，方便調試
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
    width: 400px;
    margin: 80px auto;
    background: linear-gradient(135deg, #a2dff7, #ffecb3);
    border-radius: 16px;
    padding: 40px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    overflow: hidden;
  }
  
  /* 表單標題 */
  .form-title {
    text-align: center;
    color: #333;
    font-size: 1.8rem;
    font-weight: 600;
    margin-bottom: 30px;
    text-transform: uppercase;
  }
  
  /* 註冊表單 */
  .register-form {
    display: flex;
    flex-direction: column;
  }
  
  /* 單個表單項 */
  .form-group {
    margin-bottom: 20px;
  }
  
  /* 表單標籤 */
  .form-group label {
    font-size: 0.95rem;
    color: #555;
    font-weight: 500;
    margin-bottom: 8px;
  }
  
  /* 表單輸入框 */
  .form-group input {
    padding: 12px;
    border: 1px solid #ccc;
    border-radius: 8px;
    width: 100%;
    font-size: 1rem;
    outline: none;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
  }
  
  /* 輸入框焦點效果 */
  .form-group input:focus {
    border-color: #25a294;
    box-shadow: 0 0 8px rgba(37, 162, 148, 0.2);
  }
  
  /* 提交按鈕 */
  .submit-button {
    padding: 14px;
    background-color: #25a294;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1.1rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
    width: 100%;
  }
  
  .submit-button:hover {
    background-color: #00796b;
  }
  
  /* 按鈕區域 */
  .auth-buttons {
    display: flex;
    justify-content: center;
    margin-top: 20px;
  }
  
  /* 其他登錄或註冊按鈕 */
  .auth-buttons button {
    padding: 12px 18px;
    border: none;
    border-radius: 25px;
    background-color: #4CAF50;
    color: white;
    cursor: pointer;
    font-size: 1rem;
    margin-left: 10px;
    transition: background-color 0.3s, transform 0.2s;
  }
  
  .auth-buttons button:hover {
    background-color: #45a049;
    transform: translateY(-2px);
  }
  
  .auth-buttons button:active {
    transform: translateY(0);
  }
  </style>
  
