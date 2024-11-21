<template>
  <div class="login-container">
    <h2 class="form-title">Sign In</h2>
    <form @submit.prevent="handleLogin" class="login-form">
      <div class="form-group">
        <label for="username">使用者名稱</label>
        <input type="text" v-model="username" id="username" required autocomplete="username" />
      </div>
      <div class="form-group">
        <label for="password">密碼</label>
        <input type="password" v-model="password" id="password" required autocomplete="current-password" />
      </div>
      <div class="form-footer">
        <div class="remember-me">
          <input type="checkbox" id="remember" v-model="rememberMe" />
          <label for="remember">記住我?</label>
        </div>
        <a href="#" class="forgot-password">忘記密碼?</a>
      </div>
      <button type="submit" class="submit-button" @click="getUserData">SIGN IN</button>
      <div class="social-login">
        <p>使用社交媒體登入</p>
        <div class="social-buttons">
          <button type="button" @click="handleGoogleLogin" class="social-button google-button">
            <i class="fab fa-google social-icon"></i> Google
          </button>
          <button type="button" @click="handleFbLogin" class="social-button fb-button">
            <i class="fab fa-facebook social-icon"></i> Facebook
          </button>
          <button type="button" @click="handleLineLogin" class="social-button line-button">
            <i class="fab fa-line social-icon"></i> Line
          </button>
        </div>
      </div>
    </form>
  </div>
</template>
<script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        username: '',
        password: '',
        message: "",
        rememberMe: false, // 記住我選項
        user: null, // 用戶資料
      };
    },
    methods: {
      async handleLogin() {
        try {
          const response = await axios.post("http://127.0.0.1:5000/login", {
            username: this.username,
            password: this.password,
          });
          
          console.log('Login response:', response.data); // 確認登入回應

          if (response.status === 200) {
            this.message = `登入成功！歡迎來到ecoenjoy，${this.username}`;
           
            // 儲存 Token 和用戶資料到 localStorage 或 sessionStorage
            localStorage.setItem('token', response.data.token);
            localStorage.setItem('username', response.data.user.username);
            localStorage.setItem('email', response.data.user.email);

            // 更新 UI 顯示用戶資料
            this.username = response.data.user.username;
            this.email = response.data.user.email;

            setTimeout(() => {
              this.$router.push("/"); // 導向主頁或其他頁面
            }, 2000);
          }
        } catch (error) {
          this.message = error.response?.data?.message || "登入失敗，請檢查用戶名和密碼";
        }
        alert(this.message);
      },
      async getUserData() {
      try {
        const token = localStorage.getItem("token");
        if (!token) return;

        const response = await axios.get('http://localhost:5000/user', {
          headers: {
            Authorization: `Bearer ${token}`  // 確保這裡的 token 正確
          }
        });
        console.log('用戶資料:', response.data); // 確認用戶資料回應
        this.user = response.data.user; // 儲存用戶資料
      } catch (error) {
        console.error('獲取用戶資料失敗:', error.response ? error.response.data : error.message);
        localStorage.removeItem("token");
        alert('獲取用戶資料失敗，請稍後再試。');
      }
    },

      handleGoogleLogin() {
        alert('使用 Google 登入');
      },
      handleFbLogin() {
        alert('使用 Facebook 登入');
      },
      handleLineLogin() {
        alert('使用 Line 登入');
      },
    },
  };
</script>
  
<style scoped>
  .login-container {
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
  
  .login-form {
    display: flex;
    flex-direction: column;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .form-group label {
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  .form-group input {
    padding: 10px;
    border: 1px solid #5b3a3a;
    border-radius: 8px;
  }
  
  .form-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .remember-me {
    display: flex;
    align-items: center;
  }
  
  .forgot-password {
    color: #00796b;
    text-decoration: none;
    font-size: 0.9em;
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
  
  .social-login {
    margin-top: 20px;
    text-align: center;
  }
  
  .social-buttons {
    display: flex;
    justify-content: center;
    margin-top: 10px;
  }
  
  .social-button {
    margin: 0 5px;
    padding: 10px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    display: flex;
    align-items: center;
  }
  
  .google-button {
    background-color: #db4437;
    color: white;
  }
  
  .fb-button {
    background-color: #4267b2;
    color: white;
  }
  
  .line-button {
    background-color: #00c300;
    color: white;
  }
  
  .social-icon {
    margin-right: 5px;
  }
</style>
