<<<<<<< HEAD
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
      <h3>菜單</h3>
      <div v-for="item in menu" :key="item.id" class="menu-item">
        <img :src="item.image" alt="菜品圖片" class="menu-image" />
        <div class="item-details">
          <h4>{{ item.name }}</h4>
          <p>{{ item.description }}</p>
          <span class="price">{{ item.price }} 元</span>

          <!-- 加入購物車的按鈕 -->
          <button @click="addToCart(item)" class="add-to-cart-button">加入購物車</button>
          
            <!-- 顯示評論區 -->
          <div v-if="item.reviews && item.reviews.length">
            <h5>評論</h5>
            <div v-for="review in item.reviews" :key="review.id" class="review">
              <p><strong>{{ review.user_name }}:</strong> {{ review.content }}</p>
              <div class="rating">
                <span v-for="n in review.rating" :key="n">⭐</span> 
              </div>
            </div>
            <button @click="toggleShowAllReviews(item)" v-if="!item.showAllReviews">
              查看更多評論
            </button>
            <div v-if="item.showAllReviews">
              <!-- 顯示更多評論 -->
              <button @click="toggleShowAllReviews(item)">收起評論</button>
            </div>
          </div>
          <!-- 顯示寫評論的功能 -->
          <div v-if="isLoggedIn">
            <button @click="openReviewModal(item)">寫評論</button>
          </div>
        </div>
      </div>
    </div>
    <p v-else>請選擇一間餐廳以查看菜單。</p>

    <div class="order-summary" v-if="cart.length">
      <h3>訂單總覽</h3>
      <div class="cart-item" v-for="(item, index) in cart" :key="index">
        <span>{{ item.name }} - {{ item.quantity }} x {{ item.price }} 元</span>
        <button @click="removeFromCart(index)" class="remove-button">移除</button>
      </div>
      <p class="total-price">總價: {{ totalPrice }} 元</p>

      <!-- 付款方式選擇 -->
      <div class="payment-method">
        <label>
          <input type="radio" v-model="paymentMethod" value="cash"> 現金
        </label>
        <label>
          <input type="radio" v-model="paymentMethod" value="credit_card"> 信用卡
        </label>
      </div>


      <!-- 信用卡資料 -->
      <div v-if="paymentMethod === 'credit_card'">
        <label for="credit-card-number">信用卡號：</label>
        <input type="text" id="credit-card-number" v-model="creditCardNumber" placeholder="輸入信用卡號" />
        <span v-if="!isCardValid" class="error-message">信用卡號格式不正確</span>
      </div>
    
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
      };
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

      // 執行結帳操作
      async checkout() {
        if (this.cart.length === 0) {
          alert("購物車為空，請先選擇商品！");
          return;
        }

        if (this.paymentMethod === 'credit_card' && !this.isCardValid) {
          alert("信用卡號格式不正確或尚未填寫！請檢查後再試。");
          return;
        }

        // 進行結帳流程
        this.loadingCheckout = true;
        const totalAmount = this.totalPrice;
        
        try {
          const response = await axios.post("http://127.0.0.1:5000/checkout", {
            cart: this.cart,
            totalPrice: totalAmount,
          });

          if (response.status === 200) {
            if (this.paymentMethod === 'cash') {
              alert("餐點送達付款即可，祝您用餐愉快！");
            } else {
              alert("結帳成功！");
            }
            this.cart = []; // 結帳後清空購物車
          } else {
            alert("結帳失敗，請稍後再試！");
          }
        } catch (error) {
          console.error("結帳錯誤:", error);
          alert("結帳時發生錯誤，請稍後再試！");
        } finally {
          this.loadingCheckout = false; // 完成結帳
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
  font-weight: bold;
  color: #d9534f;
}

.add-to-cart-button {
  background: linear-gradient(to right, #5cb85c, #4cae4c); /* 漸變綠色 */
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

.order-summary {
  margin-top: 20px;
  background-color: rgba(255, 255, 255, 0.9); 
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
  border: 2px solid #343a40; 
}

.cart-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.remove-button {
  background-color: #d9534f; 
  color: white;
  border: none;
  padding: 5px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.remove-button:hover {
  background-color: #c9302c; 
}

.total-price {
  font-weight: bold;
  margin-top: 10px;
}

.checkout-button {
  background: linear-gradient(to right, #0275d8, #0056b3); /* 藍色漸變 */
  color: white;
  border: none;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
  transition: background-color 0.3s;
}

.checkout-button:hover {
  background: linear-gradient(to right, #0056b3, #004494); 
}
</style>
=======
<template>
  <div class="delivery">
    <h2>外送</h2>
    <select v-model="selectedRestaurant" @change="fetchMenu" class="restaurant-select">
      <option disabled value="">選擇餐廳</option>
      <option v-for="restaurant in restaurants" :key="restaurant.id" :value="restaurant.name">
        {{ restaurant.name }}
      </option>
    </select>

    <div class="menu-items" v-if="menu.length">
      <h3>菜單</h3>
      <div class="menu-item" v-for="item in menu" :key="item.id">
        <img :src="item.img_url" alt="菜品圖片" class="menu-image" />
        <div class="item-details">
          <h4>{{ item.name }}</h4>
          <p>{{ item.description }}</p>
          <span class="price">{{ item.price }} 元</span>

          <!-- 加入購物車的按鈕 -->
          <button @click="addToCart(item)" class="add-to-cart-button">加入購物車</button>
        </div>
      </div>
    </div>
    <p v-else>請選擇一間餐廳以查看菜單。</p>

    <div class="order-summary" v-if="cart.length">
      <h3>訂單總覽</h3>
      <div class="cart-item" v-for="(item, index) in cart" :key="index">
        <span>{{ item.name }} - {{ item.quantity }} x {{ item.price }} 元</span>
        <button @click="removeFromCart(index)" class="remove-button">移除</button>
      </div>
      <p class="total-price">總價: {{ totalPrice }} 元</p>

      <!-- 付款方式選擇 -->
      <div class="payment-method">
        <label>
          <input type="radio" v-model="paymentMethod" value="cash"> 現金
        </label>
        <label>
          <input type="radio" v-model="paymentMethod" value="credit_card"> 信用卡
        </label>
      </div>


      <!-- 信用卡資料 -->
      <div v-if="paymentMethod === 'credit_card'">
        <label for="credit-card-number">信用卡號：</label>
        <input type="text" id="credit-card-number" v-model="creditCardNumber" placeholder="輸入信用卡號" />
        <span v-if="!isCardValid" class="error-message">信用卡號格式不正確</span>
      </div>
    
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
    //#############################################
    created() {
      // 嘗試從 localStorage 載入登入狀態
      const userToken = localStorage.getItem("token");
      const userId = localStorage.getItem("id");
      console.log(userToken)
      console.log(userId)
      if (userToken && userId) {
        this.isLoggedIn = true;
        this.token = userToken;
        this.userId = parseInt(userId);
      }
    },
    //##############################################
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

      // 執行結帳操作(更新)##########################################################
      async checkout() {
        if (!this.cart.length) {
          alert("購物車為空，無法結帳");
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
          // 如果已登入，附加用戶 ID 和 Token
          if (this.isLoggedIn) {
            orderData.user_id = this.userId; // 傳遞用戶 ID
          }
          console.log(this.isLoggedIn)
          console.log(this.token)
          // 設定請求頭部（包含 Token）
          const headers = {};
          if (this.isLoggedIn && this.token) {
            headers.Authorization = `Bearer ${this.token}`;
          }
          // 發送 POST 請求到後端
          const response = await axios.post("http://127.0.0.1:5000/checkout", orderData, { headers });

          if (response.status === 200) {
            alert("結帳成功！");
            // 清空購物車
            this.cart = [];
          } else {
            alert("結帳失敗：" + (response.data.error || "未知錯誤"));
          }
        } catch (error) {
          console.error("結帳過程中發生錯誤：", error.response?.data || error.message);
          alert("結帳過程中發生錯誤，請稍後再試。");
        }
      },
      //################################################################################
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
  font-weight: bold;
  color: #d9534f;
}

.add-to-cart-button {
  background: linear-gradient(to right, #5cb85c, #4cae4c); /* 漸變綠色 */
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

.order-summary {
  margin-top: 20px;
  background-color: rgba(255, 255, 255, 0.9); 
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
  border: 2px solid #343a40; 
}

.cart-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.remove-button {
  background-color: #d9534f; 
  color: white;
  border: none;
  padding: 5px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.remove-button:hover {
  background-color: #c9302c; 
}

.total-price {
  font-weight: bold;
  margin-top: 10px;
}

.checkout-button {
  background: linear-gradient(to right, #0275d8, #0056b3); /* 藍色漸變 */
  color: white;
  border: none;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
  transition: background-color 0.3s;
}

.checkout-button:hover {
  background: linear-gradient(to right, #0056b3, #004494); 
}
</style>

>>>>>>> views/delivery
