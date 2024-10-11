<template>
  <div class="root">
    <div class="sidebar" :class="{ active: sidebarActive }">
      <div class="user-info">
        <div class="user-icon">⛄</div>
        <div class="username">
          <!-- 只有在 user 存在時名稱 -->
          <a href="#" v-if="user" @click="handleUsernameClick">{{ user.username }}</a>
          <span v-else>訪客</span> 
        </div>
      </div>
      <nav>
        <ul>
          <li><router-link to="/profile">會員資料</router-link></li>
          <li><router-link to="/dietary-suggestions">個人飲食建議</router-link></li>
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
        <div class="cart-icon" @click="toggleCart">🛒</div> <!-- 購物車清單 -->
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
import { onMounted, ref, computed } from "vue"; // 整合 ref 和 computed
import { useRouter } from "vue-router"; 
import axios from "axios";

export default {
  setup() {
    const router = useRouter(); // 獲取 router 實例
    const user = ref(null); 
    const sidebarActive = ref(false);
    const json_maincats = ref([]); 
    const maincat_selected = ref(""); // 用於存儲選中的主類別
    const offers = ref(""); 
    const searchQuery = ref('');
    const isCartVisible = ref(false); // 購物車顯示
    
    const toggleCart = () => {
        isCartVisible.value = !isCartVisible.value;
    };

    const cartItems = ref([
      { id: 1, name: '商品 A', quantity: 2 },
      { id: 2, name: '商品 B', quantity: 1 },
      { id: 3, name: '商品 C', quantity: 3 },
      // 可以根據需要添加更多商品
    ]);
    
    const filteredCartItems = computed(() => {
      if (!searchQuery.value) {
        return cartItems.value;
      }
      return cartItems.value.filter(item =>
        item.name.toLowerCase().includes(searchQuery.value.toLowerCase())
      );
    });

    const removeItem = (id) => {
      cartItems.value = cartItems.value.filter(item => item.id !== id);
    };

    const toggleSidebar = () => {
      sidebarActive.value = !sidebarActive.value;
    };

    const handleProfileClick = () => {
        alert('個人資料被點擊');
    };

    const handleDietarySuggestionsClick = () => {
      alert('個人飲食建議');
    };

    const handleNutritionQuery = () => {
      alert('查詢結果');
    };

    const handleLatestOffersClick = () => {
       alert('最新優惠');
    };
    
    const getUserData = () => {
      const storedUsername = sessionStorage.getItem('username');
      if (storedUsername) {
        user.value = { username: storedUsername }; // 使用 sessionStorage 中的用戶資料
      } else {
        user.value = null; // 如果沒有用戶資料，設置為 null
        console.log('未找到用戶，顯示訪客');
      }
    };

    const handleSignOutClick = async () => {
      if (confirm("確定要登出嗎？")) {
        try {
          const token = sessionStorage.getItem('token');
          if (!token) {
            alert('未找到有效的 Token');
            return;
          }

          // 發送登出請求
          const response = await axios.post('http://localhost:5000/logout', {}, {
            headers: {
              Authorization: `Bearer ${token}`
            }
          });

          if (response.status === 200) {
            // 清空用戶信息
            user.value = null; // 清空用戶資料
            sessionStorage.removeItem('token'); // 清除 token
            sessionStorage.removeItem('username'); // 清除用戶名
            
            // 更新用戶狀態
            getUserData(); // 更新用戶狀態為「訪客」

            // 導向登入頁面
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
        json_maincats.value = response.data; // 設定主類別資料
          if (json_maincats.value.length > 0) {
            maincat_selected.value = json_maincats.value[0].id; // 預設選擇第一個類別
          }
        } catch (error) {
        console.error("獲取主類別失敗:", error);
      }
    };

  //獲取優惠資料
  const get_all_offers = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/offers"); // 獲取優惠資料
      offers.value = response.data; // 設定優惠資料
    } catch (error) {
      console.error("獲取優惠資料失敗:", error);
    }
  };
  
    onMounted(() => {
      get_all_maincat(); //主類別
      get_all_offers();// 獲取優惠資料
      getUserData();
    });
       


    return {
      user, 
      sidebarActive,
      json_maincats,
      maincat_selected,
      offers, 
      toggleSidebar,
      handleProfileClick,
      handleLatestOffersClick,
      handleDietarySuggestionsClick,
      handleNutritionQuery,
      handleSignOutClick,
      cartItems,
      searchQuery,
      isCartVisible,
      toggleCart,
      filteredCartItems,
      removeItem,
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
  font-size: 20px; /* 調整商品名稱的大小 */
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
    background: linear-gradient(135deg, #f1efef, #a3d77c);
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
