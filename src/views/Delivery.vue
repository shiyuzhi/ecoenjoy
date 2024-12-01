<template>
  <div class="delivery">
    <h2>外送</h2>
    <select v-model="selectedRestaurant" @change="fetchMenu" class="restaurant-select">
      <option disabled value="">選擇餐廳</option>
      <option v-for="restaurant in restaurants" :key="restaurant.id" :value="restaurant.name">
        {{ restaurant.name }}
      </option>
    </select>

    <div v-if="menu.length && !loadingMenu" class="menu-items">
      <!-- 餐廳資訊按鈕 -->
      <button @click="viewStore(selectedRestaurant)" class="view-store-button">
        餐廳資訊
      </button>
      <h3>菜單</h3>
      <div v-for="item in menu" :key="item.id" class="menu-item">
        <img :src="item.img_url" alt="菜品圖片" class="menu-image" />
        <div class="item-details">
          <h4>{{ item.name }}</h4>
          <p>{{ item.description }}</p>
          <span class="price">{{ Math.round(item.price) }} 元</span>
          <!-- 加入購物車的按鈕 -->
          <button @click="addToCart(item)" class="add-to-cart-button">加入購物車</button>
        </div>
      </div>
    </div>
    <p v-else>請選擇一間餐廳以查看菜單。</p>

    <div class="order-summary" v-if="cart.length">
      <h3>訂單總覽</h3>
      <div class="cart-item" v-for="(item, index) in cart" :key="index">
        <span>{{ item.name }} - {{ item.quantity }} x {{ Math.round(item.price) }} 元</span>
        <button @click="removeFromCart(index)" class="remove-button">移除</button>
      </div>
      
      <p class="total-price">總價: {{ totalPrice }} 元</p>
    
      <h4>送餐資訊確認</h4>
      <!-- 取餐人姓名 -->
      <div class="form-group">
        <label for="delivery-name">取餐人姓名：</label>
        <input type="text" id="delivery-name" v-model="deliveryName" placeholder="輸入姓名" required />
      </div>
    
      <!-- 外送地址 -->
      <div class="form-group">
        <label for="delivery-address">外送地址：</label>
        <input type="text" id="delivery-address" v-model="deliveryAddress" placeholder="輸入外送地址" required />
      </div>
    
      <!-- 電話 -->
      <div class="form-group">
        <label for="delivery-phone">電話：</label>
        <input type="text" id="delivery-phone" v-model="deliveryPhone" placeholder="輸入電話" required />
      </div>
    
     <!-- 付款方式選擇 -->
    <div class="payment-method">
      <button @click="paymentMethod = 'cash'" :class="{'active': paymentMethod === 'cash'}">現金</button>
      <button @click="paymentMethod = 'credit_card'" :class="{'active': paymentMethod === 'credit_card'}">信用卡</button>
    </div>
    
      <!-- 信用卡資料 -->
      <div v-if="paymentMethod === 'credit_card'" class="form-group">
        <label for="credit-card-number">信用卡號：</label>
        <input type="text" id="credit-card-number" v-model="creditCardNumber" placeholder="輸入信用卡號" />
        <span v-if="!isCardValid" class="error-message">信用卡號格式不正確</span>
      </div>
    
      <!-- 結帳按鈕 -->
      <button @click="checkout" :disabled="isCheckoutDisabled" class="checkout-button">結帳</button>
    </div>
        <p v-else>尚未添加任何商品到購物車。</p>
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
        creditCardNumber: '',
        paymentMethod: 'cash',  // 預設值設定為 'cash'
        isCardValid: true,
        loadingMenu: false, 
        loadingCheckout: false, 
        isLoggedIn: false, // 是否已登入
        token: null, // 儲存 JWT token（若登入）
        userId: null, // 用戶 ID (可從登入時設置)
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
    },

    methods: {
      // 獲取餐廳資料
      async fetchRestaurants(maincatId) {
        if (!maincatId) return this.restaurants = [];
        
        try {
          const response = await axios.get(`http://127.0.0.1:5000/subcat/${maincatId}`);
          this.restaurants = response.data;
        } catch (error) {
          console.error("獲取餐廳資料失敗:", error);
          this.restaurants = [];
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
        const existingItem = this.cart.find(cartItem => cartItem.id === item.id);
        if (existingItem) {
          existingItem.quantity += 1; // 若商品已存在，數量+1
        } else {
          this.cart.push({ ...item, quantity: 1 }); // 新商品加入購物車
        }
      },

      // 從購物車中移除商品
      removeFromCart(index) {
        this.cart.splice(index, 1); // 刪除指定索引的商品
      },

      // 驗證信用卡號格式
      validateCard() {
        const regex = /^[0-9]{16}$/; // 基本的信用卡號驗證，16位數字
        this.isCardValid = regex.test(this.creditCardNumber);
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

      // 執行結帳操作
      async checkout() {
        if (!this.cart.length) {
          alert("購物車為空，無法結帳");
          return;
        }

        // 檢查是否登入，未登入則跳轉至登入頁面
        if (!this.isLoggedIn) {
          alert("請先登入！");
          return;
        }

        try {
          // 構造要發送的訂單數據
          const orderData = {
            user_id: this.userId, // 傳遞用戶 ID
            cart: this.cart.map(item => ({
              info_id: item.id, // 商品的 ID
              name: item.name,
              quantity: item.quantity,
              price: item.price,
            })),
          };

          // 設定請求頭部（包含 Token）
          const headers = {};
          if (this.isLoggedIn && this.token) {
            headers.Authorization = `Bearer ${this.token}`;
          }

          // 發送 POST 請求到後端
          const response = await axios.post("http://127.0.0.1:5000/checkout", orderData, { headers });

          if (response.status === 200) {
            alert("結帳成功！");
            this.cart = []; // 清空購物車
          } else {
            alert("結帳失敗：" + (response.data.error || "未知錯誤"));
          }
        } catch (error) {
          console.error("結帳過程中發生錯誤：", error.response?.data || error.message);
          alert("結帳過程中發生錯誤，請稍後再試。");
        }
      },
    },

    // 頁面加載時，根據選擇的主類別加載餐廳
    mounted() {
      this.fetchRestaurants(this.maincat_selected);
      if (!this.paymentMethod) {
        this.paymentMethod = 'cash';
      }
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

</style>