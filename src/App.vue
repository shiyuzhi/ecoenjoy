<template>
  <div class="root">
    <div class="sidebar" :class="{ active: sidebarActive }">
      <div class="user-info">
        <div class="user-icon">⛄</div>
        <div class="username">
          <span v-if="user">{{ user.username }}</span>
          <!-- <a href="#" v-if="user" @click="handleUsernameClick">{{ user.username }}</a> -->
          <span v-else>訪客</span> 
        </div>
      </div>
      <nav aria-label="主要導航">
        <ul>
          <li><router-link to="/profile">會員資料</router-link></li>
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
        <div class="cart-icon" @click="toggleCart">🛒</div>
      </header>

      <div v-if="isCartVisible" class="cart">
        <h1>購物車清單</h1>
        <div class="search-bar">
          <input type="text" v-model="searchQuery" @keyup.enter="handleSearch" placeholder="搜尋商品" />
        </div>
        <ul>
          <li v-for="item in filteredCartItems" :key="item.id">
            {{ item.name }} - 數量: {{ item.quantity }}
            <button @click="removeItem(item.id)">刪除</button>
          </li>
        </ul>
        <p v-if="filteredCartItems.length === 0">購物車是空的</p>
      </div>

      <div class="content">
        <div class="tabs">
          <router-link to="/delivery"><button>外送</button></router-link>
          <router-link to="/pickup"><button>自取</button></router-link>
          <router-link to="/community"><button>社群</button></router-link>
          <router-link to="/custom-menu"><button>自定義菜單</button></router-link>
        </div>
        <router-view></router-view>

        <h3>餐廳推薦</h3>
        <div class="restaurant-slider">
          <div class="restaurant-item">餐廳 1</div>
          <div class="restaurant-item">餐廳 2</div>
          <div class="restaurant-item">餐廳 3</div>
          <div class="restaurant-item">餐廳 4</div>
          <div class="restaurant-item">餐廳 5</div>
        </div>

        <!-- 營養查詢區域 -->
        <div class="nutrition-query-container">
          <h1 class="nutrition-title">營養需求</h1>
      
          <!-- 營養素選擇區域 -->
          <div>
            <div class="nutrition-field" v-for="nutrient in nutrients" :key="nutrient.key">
              <label>{{ nutrient.label }}:</label>
              <button 
                @click="selectNutrient(nutrient.key, 'high')" 
                :class="{'selected': selectedNutrients[nutrient.key] === 'high'}">高</button>
              <button 
                @click="selectNutrient(nutrient.key, 'low')" 
                :class="{'selected': selectedNutrients[nutrient.key] === 'low'}">低</button>
            </div>
      
            <!-- 查詢按鈕 -->
            <button @click="fetchFoods" class="query-button">查詢</button>
            <!-- 重置按鈕 -->
            <button @click="resetSelections" class="reset-button">重置</button>
          </div>
      
          <!-- 查詢結果區域 -->
          <div class="query-results" v-if="queryResults.length > 0">
            <h4>推薦結果:</h4>
            <ul>
              <li v-for="item in queryResults" :key="item.id">
                {{ item.name }} - 蛋白質: {{ item.protein }}g, 熱量: {{ item.calories }}kcal, 脂質: {{ item.fat }}g, 碳水: {{ item.carbo }}g,餐廳: {{ item.restaurant_name}}
              </li>
            </ul>
          </div>
          <p v-else-if="queried" class="no-results">沒有符合條件的食物</p>
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
  import { ref, computed, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import axios from 'axios';
  import logo from './assets/LOGO.png'; 
  import pizzaImage from './assets/PIZZA.jpg';
  import chickenImage from './assets/CHICKEN.jpg';
  import { provide } from 'vue';


  export default {
    setup() {
      const router = useRouter();
      const user = ref(null);
      const sidebarActive = ref(false);
      const json_maincats = ref([]); 
      const maincat_selected = ref(""); 
      const offers = ref([]); 
      const searchQuery = ref('');
      const isCartVisible = ref(false); 
  
      const toggleCart = () => {
        isCartVisible.value = !isCartVisible.value;
      };
  
      const queryResults = ref([]);
      const queried = ref(false);
      const selectedNutrients = ref({ protein: null, calories: null, fat: null, carbo: null });
  
      const nutrients = [
        { key: 'protein', label: '蛋白質' },
        { key: 'calories', label: '熱量' },
        { key: 'fat', label: '脂質' },
        { key: 'carbo', label: '碳水' }
      ];
  
      const cartItems = ref([
        { id: 1, name: '商品 A', quantity: 2 },
        { id: 2, name: '商品 B', quantity: 1 },
        { id: 3, name: '商品 C', quantity: 3 },
      ]);
      
      const filteredCartItems = computed(() => {
        if (!searchQuery.value) {
          return cartItems.value;
        }
        return cartItems.value.filter(item =>
          item.name.toLowerCase().includes(searchQuery.value.toLowerCase())
        );
      });
  
      const removeItem = (itemId) => {
        cartItems.value = cartItems.value.filter(item => item.id !== itemId);
      };
  
      const toggleSidebar = () => {
        sidebarActive.value = !sidebarActive.value;
      };
  
      const getUserData = () => {
        const storedUsername = sessionStorage.getItem('username');
        user.value = storedUsername ? { username: storedUsername } : null;
      };

      // 獲取當前用戶資訊####################################################
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
      //######################################################################
      const handleSignOutClick = async () => {
        if (confirm("確定要登出嗎？")) {
          try {
            const token = localStorage.getItem('token');
            if (!token) {
              alert('未找到有效的 Token');
              return;
            }
  
            const response = await axios.post('http://localhost:5000/logout', {}, {
              headers: { Authorization: `Bearer ${token}` }
            });
  
            if (response.status === 200) {
              user.value = null; 
              localStorage.removeItem('token');
              localStorage.removeItem('username');
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
      
       // 營養素的高低分類
      const selectNutrient = (nutrient, level) => {
        if (selectedNutrients.value[nutrient] === level) {
          selectedNutrients.value[nutrient] = null; // 取消選擇
        } else {
          selectedNutrients.value[nutrient] = level;
        }
      };

      // 重置所有選擇
      const resetSelections = () => {
        selectedNutrients.value = { protein: null, calories: null, fat: null, carbo: null };
        queryResults.value = [];
        queried.value = false;
      };
      
      const fetchFoods = async () => {
        queried.value = true;
        const hasSelectedNutrients = Object.values(selectedNutrients.value).some(level => level !== null);
        if (!hasSelectedNutrients) {
            alert("請選擇至少一個營養素");
            return;
        }
        try {
            const params = new URLSearchParams();
            for (const [nutrient, level] of Object.entries(selectedNutrients.value)) {
                if (level) {  
                    params.append('nutrient', nutrient);
                    params.append('level', level);
                }
            }
            const response = await axios.get(`http://localhost:5000/foods?${params.toString()}`);
            if (response.data.message) {
                alert(response.data.message);
                queryResults.value = [];
            } else {
                queryResults.value = response.data;
            }
        } catch (error) {
            console.error("查詢失敗:", error);
            alert('查詢失敗，請稍後再試。');
            queryResults.value = [];
        }
      };
  
      onMounted(() => {
        get_all_maincat();
        get_all_offers();
        //getUserData();
        fetchUser();
      });
    
      return {
        user, 
        sidebarActive,
        json_maincats,
        maincat_selected,
        offers, 
        toggleSidebar,
        handleSignOutClick,
        cartItems,
        searchQuery,
        isCartVisible,
        toggleCart,
        filteredCartItems,
        removeItem,
        queryResults,
        queried,
        selectedNutrients,
        selectNutrient,
        fetchFoods,
        nutrients,
        resetSelections,
        logo,
        pizzaImage,
        chickenImage,
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

.nutrition-query-container {
  max-width: 500px;
  margin: 0 auto;
  padding: 50px;
  background-color: #c8fff9;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.nutrition-title {
  text-align: center;
  font-size: 24px;
  margin-bottom: 30px;
  color: #2e1515;
}

.nutrition-field {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.nutrition-field label {
  flex: 1;
  font-size: 18px;
  color: #555;
}

.nutrition-button {
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  background-color: #4caf50;
  color: white;
  font-size: 16px;
  cursor: pointer;
  margin-left: 10px;
  transition: background-color 0.3s;
}

.nutrition-button:hover {
  background-color: #45a049;
}


.selected {
  background: linear-gradient(to right, #81b5ea, #41c44c); ;
  color: white;
}

.query-results {
  margin-top: 20px;
}

.query-results h4 {
  font-size: 20px;
  margin-bottom: 10px;
  color: #333;
}

.query-results ul {
  list-style-type: none;
  padding: 0;
}

.query-results li {
  padding: 8px;
  border-bottom: 1px solid #ddd;
}

.no-results {
  text-align: center;
  color: #090505;
  font-size: 18px;
  margin-top: 20px;
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

