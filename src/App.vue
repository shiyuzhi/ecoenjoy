<template>
  <div id="app" class="root">
    <div class="sidebar" :class="{ active: sidebarActive }">
      <div class="user-info">
        <div class="user-icon">⛄</div>
        <div class="username">
          <!-- <span v-if="user">{{ user.username }}</span> -->
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

        <H2>餐廳推薦</H2>
        <div class="restaurant-list">
          <!-- 列出每家餐廳 -->
          <div class="restaurant-item" v-for="restaurant in restaurants" :key="restaurant.id">
            <div class="image-container">
              <img v-if="restaurant && restaurant.img_url" :src="`/store/${restaurant.img_url}`" :alt="restaurant.name" class="restaurant-image" />
            </div>
            <h3>{{ restaurant.name }}</h3>
            <p>{{ restaurant.address }}</p>
            <div class="rating">
              <span class="star">⭐</span>
              <p class="avg-rating">平均評分：{{ restaurant.avg_score }}</p>
            </div>
          </div>
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
  import { ref, onMounted, computed, provide, watch } from 'vue'; 
  import { useRouter } from 'vue-router';
  import axios from 'axios';
  import logo from './assets/LOGO.png';
  import dishImage from './assets/dish1.jpg';

  export default {
    setup() {
      const router = useRouter();
      const user = ref(null);
      const sidebarActive = ref(false);
      const json_maincats = ref([]); 
      const maincat_selected = ref(""); 
      const offers = ref([]); 
      const restaurants = ref([]);  // 儲存餐廳區域資料
      const slideIndex = ref(0);  // 輪播的當前索引

      // 載入餐廳資料
      const loadTopRestaurants = async () => {
        try {
          const response = await axios.get("http://127.0.0.1:5000/api/top-restaurants");
          console.log(response.data);  // 確認回傳資料
          // 轉換 avg_score 為浮動數字
          restaurants.value = response.data.map(restaurant => ({
            ...restaurant,
            avg_score: parseFloat(restaurant.avg_score)  // 確保 avg_score 是數字
          }));
        } catch (error) {
          console.error("獲取餐廳資料失敗:", error);
        }
      };

      // 切換側邊欄
      const toggleSidebar = () => {
        sidebarActive.value = !sidebarActive.value;
      };

      // 獲取用戶資料
      const fetchUser = async () => {
        try {
          const token = localStorage.getItem('token');
          if (!token) return;

          const response = await axios.get('http://127.0.0.1:5000/user', {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          user.value = response.data.user;
        } catch (error) {
          console.error('獲取用戶資訊失敗：', error);
          localStorage.removeItem('token');
        }
      };

      // 登出處理
      const handleSignOutClick = async () => {
        if (confirm("確定要登出嗎？")) {
          try {
            const token = sessionStorage.getItem('token') || localStorage.getItem('token');
            if (!token) {
              alert('已登出');
              return;
            }

            const response = await axios.post('http://localhost:5000/logout', {}, {
              headers: { Authorization: `Bearer ${token}` }
            });

            if (response.status === 200) {
              user.value = null; 
              sessionStorage.removeItem('token');
              sessionStorage.removeItem('username');
              localStorage.removeItem('token');  // 清除本地儲存
              router.push('/login');  // 登出後跳轉至登入頁面
            }
          } catch (error) {
            console.error('登出失敗:', error.response ? error.response.data : error.message);
            alert('登出失敗，請稍後再試。');
          }
        }
      };

      // 獲取主類別資料
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

      // 提供資料給子組件
      provide("maincat_selected", maincat_selected);
      provide("get_all_maincat", get_all_maincat);

      // 獲取優惠資料
      const get_all_offers = async () => {
        try {
          const response = await axios.get("http://127.0.0.1:5000/offers");
          offers.value = response.data;
        } catch (error) {
          console.error("獲取優惠資料失敗:", error);
        }
      };

      // 控制輪播滑動
      const nextSlide = () => {
        if (restaurants.value.length > 0) {
          slideIndex.value = (slideIndex.value + 1) % restaurants.value[0].menu.length;
        }
      };

      const prevSlide = () => {
        const currentRestaurant = restaurants.value.find(r => r.id === maincat_selected.value);
        if (currentRestaurant && currentRestaurant.menu) {
          slideIndex.value = (slideIndex.value - 1 + currentRestaurant.menu.length) % currentRestaurant.menu.length;
        }
      };

      // 計算滑動位置
      const slidePosition = computed(() => {
        const currentRestaurant = restaurants.value.find(r => r.id === maincat_selected.value);
        if (currentRestaurant && currentRestaurant.menu) {
          return -slideIndex.value * 220;  
        }
        return 0;
      });

      // 當主類別選擇變動時，重新載入餐廳資料
      watch(maincat_selected, (newValue) => {
        loadTopRestaurants(); // 調用 loadTopRestaurants
      });

      // 在組件掛載時加載資料
      onMounted(() => {
        get_all_maincat();
        get_all_offers();
        fetchUser();
        loadTopRestaurants();  // 正確加載餐廳資料
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
        restaurants,  
        loadTopRestaurants, 
        dishImage,
        slidePosition,
        nextSlide,
        prevSlide,
      };
    },
  };
</script>


<style scoped>  
  .root {
    display: flex;
    height: 100%;
    width: 100%;
    flex-direction: column; 
    
  }
  
  .menu-icon {
    font-size: 24px;
    margin: 20px;
    cursor: pointer;
    position: absolute;
    top: 0;
    left: 0;
    padding: 10px;
    background-color: #8cae68;
    color: white;
    transition: transform 0.2s ease;
  }
  
  .sidebar {
    width: 300px;
    background-color: #8cae68;
    color: white;
    display: flex;
    flex-direction: column;
    align-items: center;
    position: fixed;
    height: 100%;
    top: 0;
    left: -400px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .sidebar.active {
    left: 0;
    box-shadow: 4px 0 12px rgba(0, 0, 0, 0.2);
  }
  
  @media (max-width: 768px) {
    .sidebar {
      width: 30%;
      left: -100%;
    }
  
    .sidebar.active {
      left: 0;
    }
  }
  
  .menu-icon:hover {
    transform: rotate(90deg);
  }
  
  .user-info {
    display: flex;
    align-items: center;
    flex-direction: column;
    margin-top: 60px;
  }
  
  .user-info:hover {
    transform: translateY(-5px);
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
    font-size: 1.2rem;
  }
  
  nav ul {
    list-style: none;
    padding: 0;
    text-align: center;
  }
  
  nav ul li {
    margin: 30px 0;
  }
  
  nav ul li a {
    color: white;
    text-decoration: none;
    font-size: 1.2rem;
    font-weight: 400;
    transition: color 0.3s;
  }
  
  nav ul li a:hover {
    color: #0f0a03;
  }
  
  .logo-container {
    text-align: center;
  }
  
  .logo {
    width: 100px;
    height: auto;
    max-width: 100%;
    object-fit: contain;
  }
  
  .main-content {
    margin-left: 350px; /* Leave space for the sidebar */
    padding: 20px;
    flex-grow: 1;
    overflow: auto; /* Allow scrolling inside the content */
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
  
  .section-title {
    font-size: 2rem;
    font-weight: 600;
    text-align: center;
    margin: 20px 0;
  }

.auth-buttons button, .home-btn {
  padding: 0.6em 1.2em;
  font-size: 1em;
  font-weight: 500;
  border: none;
  color: #000000;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s ease;  /* 添加平滑的變化 */
  margin: 0.5em; /* 讓按鈕之間有些間距 */
}


.auth-buttons button:hover, .home-btn:hover {
  background-color: #fff; 
  transform: translateY(-4px);  /* 按鈕向上浮動 */
}


.auth-buttons button:focus, .home-btn:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.5);  
}


.auth-buttons {
  display: flex;
  justify-content: center; /* 中央對齊 */
  gap: 1em;  /* 按鈕之間的間距 */
}

.home-btn {
  background-color: #fff9f8;  
  color: rgb(71, 44, 44);
}

.home-btn:hover {
  background-color: #aaea80;  
  transform: translateY(-4px);  
}

  .restaurant-list {
    display: flex;
    overflow-x: auto;
    gap: 30px;
    padding: 0 20px;
    scrollbar-width: thin;
  }

  .restaurant-list::-webkit-scrollbar {
    height: 8px;
  }

  .restaurant-list::-webkit-scrollbar-thumb {
    background-color: #442727;
    border-radius: 8px;
  }

  .restaurant-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: linear-gradient(#1eb8a6, #ffffff);
    border-radius: 15px;
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    padding: 15px;
    width: 300x;
    flex-shrink: 0;
  }

  .restaurant-item:hover {
    transform: translateY(-10px);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
  }

  .image-container {
    width: 100%;
    height: 200px;
    overflow: hidden;
    border-radius: 10px;
    margin-bottom: 15px;
  }

  .restaurant-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
    border-radius: 10px;
    transition: transform 0.3s ease;
  }

  .restaurant-item:hover .restaurant-image {
    transform: scale(1.05);
  }

  .restaurant-info {
    text-align: center;
  }

  .restaurant-name {
    font-size: 1.4rem;
    font-weight: bold;
    color: #333;
    margin-bottom: 8px;
  }

  .restaurant-address {
    font-size: 1rem;
    color: #777;
    margin-bottom: 12px;
  }

  /* 模態框背景 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

/* 模態框樣式 */
.modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    width: 80%;
    max-width: 800px;
    overflow-y: auto;
  }

  .close-button {
    position: absolute;
    top: 10px;
    right: 10px;
    font-size: 20px;
    cursor: pointer;
  }

  .menu-items {
    display: flex;
    flex-wrap: wrap;
  }

  .menu-item {
    display: flex;
    margin: 10px;
    width: 48%;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 10px;
    box-sizing: border-box;
  }

  .menu-item img {
    max-width: 120px;
    margin-right: 15px;
  }

  .item-details {
    flex-grow: 1;
  }

  .item-details h4 {
    margin: 0;
  }

  .price {
    font-size: 18px;
    font-weight: bold;
    color: green;
  }

  .rating {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 5px;
  }

  .star {
    color: #ffb400;
    font-size: 1.2rem;
  }

  .avg-rating {
    font-size: 1rem;
    color: #444;
  }

  
  .latest-offers {
    margin-top: 20px;
    padding: 15px;
    background-color: #ffffff;
    border: 2px solid #d4d4d4;
    border-radius: 12px;
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
    transition: color 0.3s ease;
  }

  .footer-section ul li a:hover {
    color: #80d5d1;
  }

  .footer-bottom {
  display: flex;
  justify-content: flex-end; 
  align-items: center; 
  gap: 20px;
}

.footer-bottom .social-icons {
  display: flex;
  gap: 10px; 
}

.footer-bottom .language-selector {
  margin-left: 20px; 
}

.footer-bottom p {
  margin-left: 20px; 
  text-align: right;
}
@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    position: absolute;
    top: 0;
    left: -100%; /* 初始時隱藏側邊欄 */
    transform: translateX(0);
  }

  .sidebar.active {
    left: 0; /* 顯示側邊欄時從左側滑出 */
  }

  .main-content {
    margin-left: 0; /* 沒有側邊欄時，讓內容區塊占滿整個頁面 */
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

  .food-name {
    font-size: 14px;
  }
}

</style>