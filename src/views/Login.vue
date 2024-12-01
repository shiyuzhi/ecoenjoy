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
        <a href="#" class="forgot-password" @click="handleForgotPassword">忘記密碼?</a>
      </div>      

      <!-- 忘記密碼表單 -->
      <div v-if="isForgotPasswordVisible">
        <input v-model="email" type="email" placeholder="請輸入您的電子郵件" />
        <button @click="submitForgotPassword">提交</button>
        <button @click="cancelForgotPassword">取消</button>
      </div>      

      <button type="submit" class="submit-button">SIGN IN</button>
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
        user: null, // 用戶資料
        isForgotPasswordVisible: false, // 控制是否顯示忘記密碼表單
        message: '', // 訊息顯示
      };
    },
    methods: {
       // 顯示忘記密碼表單
       handleForgotPassword() {
        this.isForgotPasswordVisible = true;
      },

      // 取消忘記密碼
      cancelForgotPassword() {
        this.isForgotPasswordVisible = false;
      },

      // 提交忘記密碼的電子郵件
      
       // 提交忘記密碼的電子郵件
       submitForgotPassword() {
        if (!this.email) {
          alert('請輸入電子郵件地址！');
          return;
        }
        
        alert(`重設密碼的郵件已發送到 ${this.email}，請查收您的郵箱。`);
        this.isForgotPasswordVisible = false;
      },


      // 登入
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
            localStorage.setItem('id', response.data.user.id);

            // 更新 UI 顯示用戶資料
            this.username = response.data.user.username;
            this.email = response.data.user.email;

            setTimeout(() => {
              console.log('正在跳轉到歷史飲食頁面');
              this.$router.push("/"); // 跳轉
            }, 2000);
          }
        } catch (error) {
          this.message = error.response?.data?.message || "登入失敗，請檢查用戶名和密碼";
        }
        alert(this.message);
      },


      async getUserData(token) {
      try {
        const response = await axios.get('http://localhost:5000/user', {
          headers: {
            Authorization: `Bearer ${token}`  // 確保這裡的 token 正確
          }
        });
        console.log('用戶資料:', response.data); // 確認用戶資料回應
        this.user = response.data.user; // 儲存用戶資料
      } catch (error) {
        console.error('獲取用戶資料失敗:', error.response ? error.response.data : error.message);
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
  /* 登入容器 */
  .login-container {
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

  .login-form {
    display: flex;
    flex-direction: column;
  }
  
  /* 單個表單項 */
  .form-group {
    margin-bottom: 20px;
  }
  

  .form-group label {
    font-size: 1rem;
    color: #555;
    font-weight: 500;
    margin-bottom: 8px;
  }
  

  .form-group input {
    padding: 12px;
    border: 1px solid #ccc;
    border-radius: 8px;
    width: 100%;
    font-size: 1rem;
    outline: none;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
  }
  

  .form-group input:focus {
    border-color: #25a294;
    box-shadow: 0 0 8px rgba(37, 162, 148, 0.2);
  }
  
  .form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}


.remember-me label {
  color: black;  /* 設定「記住我」的文字顏色為黑色 */
}

.forgot-password {
  color: #00796b;
  text-decoration: none;
  font-size: 1rem;
  font-weight: 500;
  transition: color 0.3s ease;
}

.forgot-password:hover {
  color: #004d40;
  text-decoration: underline;
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
    margin: 0 10px;
    padding: 12px 16px;
    border: none;
    border-radius: 25px;
    cursor: pointer;
    display: flex;
    align-items: center;
    font-size: 1rem;
    transition: transform 0.3s ease;
  }
  
  /* 社交按鈕懸停效果 */
  .social-button:hover {
    transform: translateY(-2px);
  }
  
  /* Google登入按鈕 */
  .google-button {
    background-color: #db4437;
    color: white;
  }
  
  /* Facebook登入按鈕 */
  .fb-button {
    background-color: #4267b2;
    color: white;
  }
  

  .line-button {
    background-color: #00c300;
    color: white;
  }
  
  
  .social-icon {
    margin-right: 8px;
  }
  </style>
  