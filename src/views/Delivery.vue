<template>
  <div class="delivery">
    <h2>外送</h2>
    <select v-model="selectedRestaurant" @change="fetchMenu" class="restaurant-select">
      <option disabled value="">選擇餐廳</option>
      <option v-for="restaurant in restaurants" :key="restaurant.id" :value="restaurant.name">{{ restaurant.name }}</option>
    </select>

    <div v-if="menu.length && !loadingMenu" class="menu-items">
      <button @click="viewStore(selectedRestaurant)" class="view-store-button">餐廳資訊</button>
      <h3>菜單</h3>
      <div v-for="item in menu" :key="item.id" class="menu-item">
        <img :src="item.img_url" alt="菜品圖片" class="menu-image" />
        <div class="item-details">
          <h4>{{ item.name }}</h4>
          <p>{{ item.description }}</p>
          <span class="price">{{ Math.round(item.price) }} 元</span>
          <button @click="viewComments(item)" class="view-comments-button">查看評論</button>
          <button @click="addToCart(item)" class="add-to-cart-button">加入購物車</button>
        </div>
      </div>
    </div>
    <p v-else>請選擇一間餐廳以查看菜單。</p>

    <div v-if="showCommentsModal" class="modal">
      <div class="modal-content">
        <!-- 左邊：菜品資訊 -->
        <div class="modal-left">
          <h2>{{ selectedMenuItem?.name }}</h2>
          <p>價格：{{ selectedMenuItem?.price }} 元</p>
          <p>熱量：{{ selectedMenuItem?.calories }} 大卡</p>
          <p>蛋白質：{{ selectedMenuItem?.protein }} 克</p>
          <p>脂肪：{{ selectedMenuItem?.fat }} 克</p>
          <p>碳水化合物：{{ selectedMenuItem?.carbo }} 克</p>
          <img :src="selectedMenuItem?.img_url" alt="菜品圖片" />
        </div>
    
        <!-- 右邊：評論列表 -->
        <div class="modal-right">
          <h3>評論</h3>
          <div v-if="loadingComments">加載中...</div>
          <ul v-else>
            <li v-for="comment in comments" :key="comment.id">
              <p><strong>{{ comment.user.username }}：</strong> {{ comment.data }}</p>
              <button @click="likeComment(comment.id)">👍 {{ comment.likes }}</button>
              <span>回覆數: {{ comment.replies }}</span>
            </li>
          </ul>
        </div>
    
        <!-- 關閉按鈕 -->
        <button class="close-button" @click="closeCommentsModal">關閉</button>
      </div>
    </div>
  </div>
</template>


<script>
  import axios from "axios";

  export default {
    inject: ["maincat_selected"],

    data() {
      return {
        selectedRestaurant: '',
        restaurants: [],
        menu: [],
        cart: [],
        loadingMenu: false,  
        isLoggedIn: false, // 是否已登入
        token: null, // 儲存 JWT token（若登入）
        userId: null, // 用戶 ID (可從登入時設置)
        showCommentsModal: false, 
        selectedMenuItem: null, 
        comments: [], 
        loadingComments: false, 
        showFoodModal: false, 
        };
     },

    created() {
      // 嘗試從 localStorage 載入登入狀態
      const userToken = localStorage.getItem("token");
      const userId = localStorage.getItem("id");

      if (userToken && userId) {
        this.isLoggedIn = true;
        this.token = userToken;
        this.userId = parseInt(userId);
      }
    },

    computed: {
      // 計算購物車的總價
      totalPrice() {
        return this.cart.reduce((total, item) => total + (item.price * item.quantity), 0);
      },

      // 計算結帳按鈕是否禁用
      isCheckoutDisabled() {
        if (this.paymentMethod === 'credit_card') {
          // 信用卡付款時，檢查卡號是否有效
          return !this.isCardValid || !this.creditCardNumber;
        }
        return this.cart.length === 0;
      },
    },

    watch: {
      // 當 maincat_selected 變動時重新加載餐廳資料
      maincat_selected(newMaincat) {
        this.fetchRestaurants(newMaincat);
      },
      creditCardNumber(newCardNumber) {
        const cardPattern = /^[0-9]{16}$/; // 假設信用卡號為16位數字
        this.isCardValid = cardPattern.test(newCardNumber);
      },
    },

    
    methods: {
      async fetchComments(foodId) {
        this.loadingComments = true; // 開始加載評論
        try {
          const response = await axios.get(`/api/comments/store/${foodId}`, {
            headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
          });
          
          const responseData = response.data;
          this.comments = responseData.comments || []; // 提取評論列表
          this.selectedMenuItem = {
            ...responseData.food,
            comments: responseData.comments, // 可選：直接將評論綁定至菜品
          };
        } catch (error) {
          console.error("Error fetching comments:", error);
          this.comments = []; // 發生錯誤時清空評論
          this.selectedMenuItem = null; // 清空菜品資訊
        } finally {
          this.loadingComments = false; // 完成加載
        }
      },
      
      async likeComment(commentId) {
        const token = localStorage.getItem("token");

        if (!token) {
          alert("請先登入才能點讚！");
          return;  // 沒有 token 時終止函數
        }

        try {
          const response = await axios.post(
            `/api/comments/like/${commentId}`,
            {},
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          );
          // 更新評論的點讚數
          const comment = this.comments.find((c) => c.id === commentId);
          if (comment) {
            comment.likes = response.data.likes;
          }
        } catch (error) {
          console.error("Error liking comment:", error);
        }
      },
      // 根據選擇的餐廳獲取菜單
      async fetchMenu() {
        if (!this.selectedRestaurant) return;

        this.loadingMenu = true; // 開始加載菜單
        try {
          const response = await axios.get(`http://127.0.0.1:5000/menu/${this.selectedRestaurant}`);
          this.menu = response.data;
        } catch (error) {
          console.error("無法載入菜單資料:", error);
          this.menu = [];
        } finally {
          this.loadingMenu = false; // 完成菜單加載
        }
      },

      // 添加商品到購物車
      addToCart(item) {
        const cart = JSON.parse(localStorage.getItem("cart")) || [];
        const existingItem = cart.find((cartItem) => cartItem.id === item.id);
        if (existingItem) {
          existingItem.quantity += 1;
        } else {
          cart.push({ ...item, quantity: 1 });
        }
        localStorage.setItem("cart", JSON.stringify(cart));
        this.updateCartCount();
        alert("添加成功！");
      },

      updateCartCount() {
        const cart = JSON.parse(localStorage.getItem("cart")) || [];
        this.cartCount = cart.reduce((sum, item) => sum + item.quantity, 0);
      },
    
      // 點擊餐廳資訊按鈕，跳轉到餐廳詳細頁
      viewStore(restaurantName) {
        const selected = this.restaurants.find(r => r.name === restaurantName);
        if (selected && selected.id) {
          this.$router.push(`/store/${selected.id}`);
        } else {
          console.error("餐廳資料無效");
        }
      },
    },
    // 頁面加載時，根據選擇的主類別加載餐廳
    mounted() {
      this.fetchRestaurants(this.maincat_selected);
    },
  };
</script>




<style scoped>
.delivery {
  padding: 20px;
  border: 2px solid #343a40; 
  border-radius: 8px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
}

.restaurant-select {
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #343a40; 
  margin-bottom: 20px;
  width: 100%;
}

.menu-items {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.menu-item {
  display: flex;
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 15px;
  background-color: rgba(255, 255, 255, 0.8); /*背景 */
  transition: box-shadow 0.3s;
}

.menu-item:hover {
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.3); /*陰影 */
}

.menu-image {
  width: 100px;
  height: 100px;
  border-radius: 5px;
  margin-right: 15px;
}

.item-details {
  flex-grow: 1;
}

.price {
  margin-right: 20px;
  font-weight: bold;
  color: #d9534f;
}

.add-to-cart-button {
  background: linear-gradient(to right, #8ee58e, #4cae4c); 
  color: white;
  border: none;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.add-to-cart-button:hover {
  background: linear-gradient(to right, #4cae4c, #45a049); 
}

/* 訂單總覽樣式 */
.order-summary {
  background-color: #fff;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: 20px auto;
}

h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 10px;
  text-align: center;
}

.cart-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 0.95rem;
}

.remove-button {
  background-color: #ff6347;
  color: white;
  border: none;
  padding: 5px 8px;
  font-size: 0.875rem;
  cursor: pointer;
  border-radius: 4px;
}

.remove-button:hover {
  background-color: #2b110c;
}

.total-price {
  font-size: 1.1rem;
  font-weight: bold;
  text-align: center;
  margin: 10px 0;
}

/* 表單樣式 */
.form-group {
  margin-top: 12px;
}

.form-group label {
  font-size: 0.9rem;
  margin-bottom: 6px;
  font-weight: 500;
}

.form-group input {
  padding: 8px;
  font-size: 0.9rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  width: 100%;
}

.form-group input:focus {
  border-color: #8CAE68;
  outline: none;
}

/* 付款方式選擇 */
.payment-method {
  margin-top: 15px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px; 
}


.payment-method button {
  padding: 10px 20px;
  font-size: 1rem;
  color: rgb(12, 7, 7);
  border: none;
  border-radius: 10px; 
  cursor: pointer; 
  transition: background-color 0.3s, transform 0.2s;
}

.payment-method button.active { 
  transform: scale(1.1); 
}

.payment-method button:hover {
  transform: scale(1.05); 
}

.payment-method input {
  transform: scale(1.2);
}

.error-message {
  color: #ff6347;
  font-size: 0.8rem;
  margin-top: 4px;
}

/* 結帳按鈕 */
.checkout-button {
  background: linear-gradient(to right, #e8ffe8, #4caea9); 
  color: rgb(22, 12, 12);
  border: none;
  padding: 10px 0;
  font-size: 1rem;
  border-radius: 6px;
  width: 100%;
  margin-top: 20px;
  cursor: pointer;
  text-align: center;
}

.checkout-button:disabled {
  background-color: #ffd2d2;
  cursor: not-allowed;
}

.checkout-button:hover {
  background-color: #15b6e8;
}

.view-store-button {
  display: inline-block;
  margin-bottom: 10px;
  padding: 10px 20px;
  font-size: 16px;
  font-weight: bold;
  color: white;
  background-color: #3897ea; 
  border: none;
  border-radius: 5px;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); 
  transition: all 0.3s ease;
}

.view-store-button:hover {
  background-color: #3f1f15; 
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15); 
  transform: scale(1.05); 
}

.view-store-button:active {
  background-color: #43180a; 
  box-shadow: none; 
  transform: scale(0.95); 
}

/* 評論模態框 */

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6); /* 半透明黑色遮罩 */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-in-out;
}


.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6); /* 半透明黑色遮罩 */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-in-out;
}

/* 模態框內容 */
.modal-content {
  display: flex;
  background: linear-gradient(135deg, #fdd297, #ffffff, #82d1ea); /* 三色漸層背景 */
  border-radius: 15px;
  padding: 25px;
  max-width: 90%;
  width: 800px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s ease-out;
  position: relative;
  max-height: 80%;
  overflow: hidden;
  color: #000000; /* 白色文字 */
}

/* 左側：菜品資訊 */
.modal-left {
  flex: 1;
  padding-right: 20px;
  border-right: 2px solid rgba(255, 255, 255, 0.4); /* 半透明白色分隔線 */
  text-align: center;
}

.modal-left img {
  width: 100%;
  border-radius: 15px;
  margin-top: 15px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.modal-left img:hover {
  transform: scale(1.05); /* 懸停放大效果 */
  box-shadow: 0 10px 20px rgba(255, 255, 255, 0.5); /* 增加陰影 */
}

.highlight {
  color: #ffe57f;
  font-weight: bold;
}

/* 右側：評論列表 */
.modal-right {
  flex: 2;
  padding-left: 20px;
  overflow-y: auto;
}

.modal-right ul {
  list-style: none;
  padding: 0;
}

.modal-right li {
  background: rgba(255, 255, 255, 0.2); /* 半透明背景 */
  margin-bottom: 15px;
  padding: 15px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.4);
  transition: box-shadow 0.3s ease, transform 0.3s ease;
}

.modal-right li:hover {
  box-shadow: 0 6px 15px rgba(255, 255, 255, 0.4); /* 懸停時陰影加強 */
  transform: translateY(-5px); /* 懸停時向上微移 */
}

.comment-header {
  display: flex;
  justify-content: space-between;
}

.comment-actions {
  display: flex;
  justify-content: flex-start;
  gap: 10px;
  margin-top: 10px;
}

.like-button,
.reply-button {
  padding: 5px 15px;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.3s ease, transform 0.2s;
}

.like-button {
  background: #ff8a65; /* 橙色背景 */
  color: #fff;
}

.like-button:hover {
  background: #ff7043; /* 濃橙色 */
  transform: scale(1.1); /* 懸停時放大 */
}

.reply-button {
  background: #4fc3f7; /* 淺藍色背景 */
  color: #fff;
}

.reply-button:hover {
  background: #29b6f6; /* 深藍色 */
  transform: scale(1.1); /* 懸停時放大 */
}

/* 按鈕樣式 */
.close-button {
  position: absolute;
  top: 15px;
  right: 15px;
  padding: 10px;
  background: #050202;
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  font-size: 18px;
  transition: background 0.3s, transform 0.2s;
}

.close-button:hover {
  background: #8f042094; /* 更深的紅色 */
  transform: scale(1.2); /* 懸停時放大 */
}

/* 動畫效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    transform: translateY(30px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
</style>