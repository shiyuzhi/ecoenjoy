<template>
  <div class="root">
    <div class="sidebar" :class="{ active: sidebarActive }">
      <div class="user-info">
        <div class="user-icon">⛄</div>
        <div class="username">
          <a href="#" v-if="user" @click="handleUsernameClick">{{ user.username }}</a>
          <span v-else>訪客</span> 
        </div>
      </div>
      <nav aria-label="主要導航">
        <ul>
          <li><router-link to="/profile">會員資料</router-link></li>
          <li><router-link to="/nutrition-query">營養需求</router-link></li>
          <li><router-link to="/dietary-suggestions">個人飲食建議</router-link></li>
          <li><router-link to="/diet-log">飲食日誌</router-link></li>
          <li><router-link to="/history-diet">歷史飲食紀錄</router-link></li>
          <li><a href="#" @click.prevent="handleSignOutClick">登出</a></li>
        </ul>
      </nav>
    </div>

    <div class="main-content">
      <header>
        <div class="menu-icon" @click="toggleSidebar">☰</div>   
        <div class="logo-container">
          <img v-if="logo" :src="logo" alt="Ecoenjoy Logo" class="logo" />
          <p v-else>圖片加載失敗</p>
        </div>
          <div class="auth-buttons">
            <router-link to="/Login">
              <button>登入</button>
            </router-link>
            <router-link to="/register">
              <button>註冊</button>
            </router-link>
          </div>
          <div class="location-selector">
            <select v-model="maincat_selected">
              <option v-for="maincat in json_maincats" :key="maincat.id" :value="maincat.id">
                {{ maincat.name }}
              </option>
            </select>
          </div>
        <div class="search-bar">
          <input type="text" placeholder="搜尋">
        </div>
         <!-- Home 按鈕 -->
        <router-link to="/">
          <button class="home-btn">首頁</button>
        </router-link>
      </header>

      <div class="content">
        <router-view></router-view>
      
        <h3>餐廳推薦</h3>
        <div class="restaurant-slider">
          <div class="restaurant-item">餐廳 1</div>
          <div class="restaurant-item">餐廳 2</div>
          <div class="restaurant-item">餐廳 3</div>
          <div class="restaurant-item">餐廳 4</div>
          <div class="restaurant-item">餐廳 5</div>
        </div>
        
        <!-- 最新優惠區域 -->
        <div class="latest-offers">
          <h2>最新優惠</h2>
          <ul>
            <li v-for="offer in offers" :key="offer.id">
              {{ offer.title }} - {{ offer.description }}
            </li>
          </ul>
        </div>

         <!-- 底部-->
        <footer>
          <div class="footer-content">
            <div class="footer-section">
              <h4>Services</h4>
              <ul>
                <li><a href="#">Contact Us</a></li>
              </ul>
            </div>
            <div class="footer-section">
              <h4>Quick Links</h4>
              <ul>
                <li><a href="#">Foods</a></li>
                <li><a href="#">Community</a></li>
              </ul>
            </div>
            <div class="footer-section">
              <h4>Legal</h4>
              <ul>
                <li><a href="#">Privacy Policy</a></li>
                <li><a href="#">Terms and Conditions</a></li>
              </ul>
            </div>
          </div>
          <div class="footer-bottom">
            <div class="social-icons">
              <a href="#"><i class="fa fa-facebook"></i></a>
              <a href="#"><i class="fa fa-instagram"></i></a>
            </div>
            <div class="language-selector">
              <select id="language" onchange="changeLanguage()">
                <option value="en">English</option>
                <option value="zh">繁體中文</option>
                <option value="es">Español</option>
                <option value="fr">Français</option>
                <option value="de">Deutsch</option>
                <option value="ja">日本語</option>
                <option value="ko">한국어</option>
                <option value="ru">Русский</option>
                <option value="it">Italiano</option>
                <option value="pt">Português</option>
                <option value="ar">العربية</option>
              </select>
            </div>
            <p>&copy; 2024 ecoenjoy. All rights reserved.</p>
          </div>
        </footer>
      </div>
    </div>
  </div>
</template>

<script>
  import { ref, onMounted, computed } from 'vue';  // 添加 computed
  import { useRouter } from 'vue-router';
  import axios from 'axios';
  import logo from './assets/LOGO.png';
  import { provide } from 'vue';

  export default {
    setup() {
      const router = useRouter();
      const user = ref(null);
      const sidebarActive = ref(false);
      const json_maincats = ref([]); 
      const maincat_selected = ref(""); 
      const offers = ref([]); 
  
      const toggleSidebar = () => {
        sidebarActive.value = !sidebarActive.value;
      };
  
      const getUserData = () => {
        const storedUsername = sessionStorage.getItem('username');
        user.value = storedUsername ? { username: storedUsername } : null;
      };
  
      const handleSignOutClick = async () => {
        if (confirm("確定要登出嗎？")) {
          try {
            const token = sessionStorage.getItem('token');
            if (!token) {
              alert('未找到有效的 Token');
              return;
            }
  
            const response = await axios.post('http://localhost:5000/logout', {}, {
              headers: { Authorization: `Bearer ${token}` }
            });
  
            if (response.status === 200) {
              user.value = null; 
              sessionStorage.removeItem('token');
              sessionStorage.removeItem('username');
              getUserData();
              router.push('/login');
            }
          } catch (error) {
            console.error('登出失敗:', error.response ? error.response.data : error.message);
            alert('登出失敗，請稍後再試。');
          }
        }
      };
  
      const get_all_maincat = async () => {
        try {
          const response = await axios.get("http://127.0.0.1:5000/maincat");
          json_maincats.value = response.data; 
          if (json_maincats.value.length > 0) {
            maincat_selected.value = json_maincats.value[0].id; 
          }
        } catch (error) {
          console.error("獲取主類別失敗:", error);
        }
      };

      // 提供 maincat_selected 和 get_all_maincat 給子組件
      provide("maincat_selected", maincat_selected);
      provide("get_all_maincat", get_all_maincat);
  
      const get_all_offers = async () => {
            try {
              const response = await axios.get("http://127.0.0.1:5000/offers");
              offers.value = response.data;
            } catch (error) {
              console.error("獲取優惠資料失敗:", error);
            }
          };
  
      onMounted(() => {
        get_all_maincat();
        get_all_offers();
        getUserData();
      });
    
      return {
        user, 
        sidebarActive,
        json_maincats,
        maincat_selected,
        offers, 
        toggleSidebar,
        handleSignOutClick,
        logo,
      };
    },
  };
</script>

  
  
<style scoped>
.root {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  width: 250px; /* 固定寬度 */
  background-color: #8CAE68;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: fixed;
  height: 100%;
  top: 0;
  left: 0;
  transition: transform 0.3s ease;
  transform: translateX(-100%);
}

.sidebar.active {
  transform: translateX(0);
}

.menu-icon {
  font-size: 24px;
  margin: 20px;
  cursor: pointer;
  position: absolute;
  top: 0;
  left: 0;
  padding: 10px;
  background-color: #8CAE68;
  color: white;
}

.user-info {
  display: flex;
  align-items: center;
  flex-direction: column;
  margin-top: 60px;
}

.user-icon {
  font-size: 50px;
}

.username {
  margin-top: 10px;
}

.username a {
  color: white;
  text-decoration: none;
}

nav ul {
  list-style: none;
  padding: 0;
  text-align: center;
}

nav ul li {
  margin: 20px 0;
}

nav ul li a {
  color: white;
  text-decoration: none;
}

.main-content {
  flex-grow: 1; 
  margin-left: 250px; 
  padding: 20px;
  overflow-y: auto; 
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.location-selector select {
  font-size: 16px;
}

.search-bar input {
  padding: 5px;
  font-size: 16px;
}

.cart {
  position: absolute;
  top: 60px;
  right: 20px;
  background: #89b35d;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  width: 250px;
  box-shadow: 0 2px 8px rgba(27, 216, 2, 0.2);
  z-index: 800;
}
.cart-icon {
  font-size: 40px;
}

.cart h1 {
  font-size: 40px; /* 可以調整標題大小 */
}

.cart li {
  font-size: 15px; /* 調整商品名稱的大小 */
}

.cart-visible {
  opacity: 1;
  transform: translateY(0);
  transition: all 0.3s ease-in-out;
}
.cart-hidden {
  opacity: 0;
  transform: translateY(-20px);
  transition: all 0.3s ease-in-out;
}

.tabs {
  display: flex;
  justify-content: space-between;
  margin: 20px 0;
}

.tabs button {
  padding: 10px;
  background-color: #8CAE68;
  color: white;
  border: none;
  cursor: pointer;
}

.restaurant-slider {
    display: flex;
    overflow-x: auto;
    padding: 30px 0;
    scroll-behavior: smooth;
}

.restaurant-item {
  min-width: 250px;
    height: 200px;
    background: linear-gradient(135deg, #f1efef, #96fa5c);
    margin-right: 20px;
    border-radius: 8px;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0 4px 10px rgba(211, 0, 0, 0.2);
    transition: transform 0.3s, box-shadow 0.6s;
}

.restaurant-item:hover {
    transform: translateY(-10px);
    box-shadow: 0 6px 15px rgba(226, 195, 195, 0.3);
}

.restaurant-item h4 {
    font-family: 'Arial', sans-serif;
    font-size: 18px;
    color: #e1dedeee;
    text-align: center;
}



.latest-offers {
  margin-top: 20px;
  padding: 15px;
  background-color: #ffffff; 
  border: 2px solid black; 
  border-radius: 10px; 
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.latest-offers h2 {
  margin-bottom: 20px;
}

.offers-list {
  padding: 0;
}

.offer-item {
  padding: 10px;
  border-bottom: 1px solid #ddd;
  transition: background-color 0.3s;
}

.offer-item:last-child {
  border-bottom: none;
}

.offer-item:hover {
  background-color: #f0f0f0;
}

.auth-buttons {
  display: flex;  
  color: #000000;                                            
}

footer {
  background-color: #1eb8a6;
  margin-top: 20px;
  color: #fff;
  padding: 15px 0;
  text-align: center;
  border-radius: 20px; 
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.footer-content {
  display: flex;
  justify-content: space-around;
  padding-bottom: 20px;
}

.footer-section h4 {
  font-weight: bold;
}

.footer-section ul {
  list-style: none;
  padding: 0;
}

.footer-section ul li {
  margin: 8px 0;
}

.footer-section ul li a {
  color: #fff;
  text-decoration: none;
  transition: color 0.3s; /* 添加過渡效果 */
}

.footer-section ul li a:hover {
  color: #f39c12; /* 懸停顏色 */
}

.footer-bottom {
  display: flex;
  justify-content: space-between; 
  align-items: center; /* 垂直置中 */
  padding: 10px; 
}
.social-icons a {
  color: #fff;
  margin-right: 10px;
  font-size: 1.5rem;
}

.language-selector select {
  background-color: #000;
  color: #fff;
  border: 1px solid #fff;
  padding: 5px;
  border-radius: 10px; 
  cursor: pointer; 
}

.language-selector select:hover {
  border-color: #f39c12; 
  transform: translateX(-5px); 
}

p {
  margin: 0;
  text-align: right;
} 

.logo-container {
  text-align: center; 
}

.logo {
  width: 100px; 
  height: auto; 
}


@media (max-width: 768px) {
  .sidebar {
    width: 100%; 
    position: relative; 
    transform: translateX(0); 
  }

  .main-content {
    margin-left: 0; 
    padding: 10px; 
  }

  .restaurant-slider {
    flex-direction: column; 
  }

  .restaurant-item {
    min-width: 100%;
    height: auto; 
    margin-bottom: 10px; 
  }


}
</style>