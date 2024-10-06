<template>
  <div class="root">
    <div class="sidebar" :class="{ active: sidebarActive }">
      <div class="user-info">
        <div class="user-icon">👤</div>
        <div class="username"><a href="#" @click="handleUsernameClick">用戶名</a></div>
      </div>
      <nav>
        <ul>
          <li><a href="#" @click="handleProfileClick">個人檔案</a></li>
          <li><a href="#" @click="handleLatestOffersClick">最新優惠</a></li>
          <li><a href="#" @click="handleDietarySuggestionsClick">個人飲食建議</a></li>
          <li><a href="#" @click.prevent="handleSignOutClick">登出</a></li>
        </ul>
      </nav>
    </div>

    <div class="main-content">
      <header>
        <div class="menu-icon" @click="toggleSidebar">☰</div>
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
        <div class="cart-icon">🛒</div>
      </header>

      <div class="content">
        <div class="tabs">
          <router-link to="/delivery"><button>外送</button></router-link>
          <router-link to="/pickup"><button>自取</button></router-link>
          <router-link to="/community"><button>社群</button></router-link>
          <router-link to="/custom-menu"><button>自定義菜單</button></router-link>
        </div>
        <router-view></router-view> <!-- 用於顯示路由內容 -->
        <h3>餐廳推薦</h3>
        <div class="restaurant-slider">
          <div class="restaurant-item">餐廳 1</div>
          <div class="restaurant-item">餐廳 2</div>
          <div class="restaurant-item">餐廳 3</div>
          <div class="restaurant-item">餐廳 4</div>
          <div class="restaurant-item">餐廳 5</div>
        </div>

        <div class="nutrition-query">
          <h3>營養價值查詢</h3>
          <input type="text" placeholder="微米化合物">
          <input type="text" placeholder="蛋白質">
          <input type="text" placeholder="膳食纖維">
          <button @click="handleNutritionQuery">查詢</button>
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
      </div>
    </div>
  </div>
</template>

<script>
  import { onMounted, ref } from "vue";
  import axios from "axios";
  
  export default {
    setup() {
      const sidebarActive = ref(false);
      const json_maincats = ref([]); 
      const maincat_selected = ref(""); // 用於存儲選中的主類別
  
      const toggleSidebar = () => {
        sidebarActive.value = !sidebarActive.value;
      };
  
      const handleProfileClick = () => {
        alert('個人檔案被點擊');
      };
  
      const handleLatestOffersClick = () => {
        alert('最新優惠被點擊');
      };
  
      const handleDietarySuggestionsClick = () => {
        alert('個人飲食建議被點擊');
      };
  
      const handleNutritionQuery = () => {
        alert('營養查詢被點擊');
      };
  
      const handleSignOutClick = async () => {
        if (confirm("確定要登出嗎？")) {
          try {
            await axios.post('/logout');
            this.$router.push('/login');
          } catch (error) {
            console.error('登出失敗:', error);
          }
        }
      };
  
      const get_all_maincat = async () => {
        try {
          const response = await axios.get("http://127.0.0.1:5000/maincat");
          json_maincats.value = response.data;  // 設定主類別資料
          if (json_maincats.value.length > 0) {
            maincat_selected.value = json_maincats.value[0].name; // 預設選擇第一個
          }
        } catch (error) {
          console.error("獲取主類別失敗:", error);
        }
      };
    
      onMounted(() => {
        get_all_maincat(); // 在組件掛載時調用函數
      });
  
      return {
        sidebarActive,
        json_maincats,
        maincat_selected,
        toggleSidebar,
        handleProfileClick,
        handleLatestOffersClick,
        handleDietarySuggestionsClick,
        handleNutritionQuery,
        handleSignOutClick,
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

.cart-icon {
  font-size: 24px;
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
}

.restaurant-item {
  min-width: 250px; 
  height: 200px; 
  background-color: #e0e0e0;
  margin-right: 20px; 
  border-radius: 8px; 
}

/* 營養查詢 */
.nutrition-query {
  margin: 20px 0;
}

.nutrition-query h3 {
  margin-bottom: 10px;
}

.nutrition-query input {
  display: block;
  margin: 10px 0;
  padding: 5px;
  width: 80%;
}

.nutrition-query button {
  padding: 10px;
  background-color: #8CAE68;
  color: white;
  border: none;
  cursor: pointer;
}

.latest-offers {
  height: 150px; 
  background-color: #e0e0e0;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 24px; 
}

.auth-buttons {
  display: flex;  
  color: #000000;                                            
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
