<template>
  <div class="pickup">
    <h2>自取</h2>

    <!-- 餐廳選擇 -->
    <select v-model="selectedRestaurant" @change="fetchMenu">
      <option disabled value="">選擇餐廳</option>
      <!-- 確保這裡使用正確的數據 -->
      <option v-for="restaurant in filteredRestaurants" :key="restaurant.id" :value="restaurant.id">
        {{ restaurant.name }}
      </option>
    </select>

    <!-- 菜單項目顯示 -->
    <div class="menu-items">
      <h3>菜單</h3>
      <div v-if="loadingMenu" class="loading">菜單加載中...</div>
      <div v-for="item in menu" :key="item.id" class="menu-item">
        <img :src="item.image" alt="菜品圖片" />
        <div>
          <h4>{{ item.name }}</h4>
          <p>{{ item.description }}</p>
          <span>{{ item.price }} 元</span>
          <button @click="addToCart(item)">加入購物車</button>
        </div>
      </div>
    </div>

    <!-- 自取時間 -->
    <div class="pickup-time">
      <label for="pickup-time">選擇自取時間:</label>
      <input type="datetime-local" id="pickup-time" v-model="pickupTime" />
    </div>

    <!-- 訂單總覽 -->
    <div class="order-summary">
      <h3>訂單總覽</h3>
      <div v-if="cart.length === 0">購物車是空的</div>
      <div v-for="(item, index) in cart" :key="index">
        {{ item.name }} - {{ item.price }} 元
        <button @click="removeFromCart(index)">移除</button>
        <button @click="increaseQuantity(item)">+</button>
        <button @click="decreaseQuantity(item)">-</button>
      </div>
      <p>總價: {{ totalPrice }} 元</p>
      <button :disabled="isCheckoutDisabled" @click="checkout">結帳</button>
      <button v-if="cart.length > 0" @click="clearCart">清空購物車</button>
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
      pickupTime: '',
      creditCardNumber: '',
      paymentMethod: 'cash',  // 預設為現金
      isCardValid: true,
      loadingMenu: false, 
      loadingCheckout: false, 
    };
  },

  computed: {
    // 計算總價
    totalPrice() {
      return this.cart.reduce((total, item) => total + (item.price * item.quantity), 0);
    },

    // 判斷結帳按鈕是否禁用
    isCheckoutDisabled() {
      if (this.paymentMethod === 'credit_card') {
        return !this.isCardValid || !this.creditCardNumber;
      }
      return this.cart.length === 0;
    },

    // 篩選餐廳的邏輯，根據需要進行過濾
    filteredRestaurants() {
      // 進行過濾
      return this.restaurants;  
    },
  },

  watch: {
    maincat_selected(newMaincat) {
      this.fetchRestaurants(newMaincat);
    },
  },

  methods: {
    // 獲取餐廳資料
    async fetchRestaurants(maincatId) {
      console.log("maincatId:", maincatId);  // 確保這裡獲取到有效的 maincatId
      if (!maincatId) return this.restaurants = [];
      
      try {
        const response = await axios.get(`http://127.0.0.1:5000/subcat/${maincatId}`);
        console.log("Fetched restaurants:", response.data); // 打印餐廳資料來確認
        if (response.data.length === 0) {
          alert("此區域沒有可用的餐廳");
          this.restaurants = [];
        } else {
          this.restaurants = response.data;
        }
      } catch (error) {
        console.error("獲取餐廳資料失敗:", error);
        alert("無法載入餐廳資料，請稍後再試！");
        this.restaurants = [];
      }
    },
   // 獲取菜單
   async fetchMenu() {
      if (!this.selectedRestaurant) return;

      this.loadingMenu = true;
      try {
        // 根據選擇的餐廳 ID 查找名稱
        const selectedRestaurantData = this.restaurants.find(restaurant => restaurant.id === this.selectedRestaurant);
        const subcatName = selectedRestaurantData ? selectedRestaurantData.name : '';

        // 如果名稱存在，就發送請求
        if (subcatName) {
          const response = await axios.get(`http://127.0.0.1:5000/menu/${subcatName}`);
          console.log("菜單資料：", response.data);

          if (response.data && Array.isArray(response.data)) {
            this.menu = response.data;
          } else {
            alert("菜單資料格式錯誤或無法加載！");
            this.menu = [];
          }
        }
      } catch (error) {
        console.error("無法載入菜單資料:", error);
        alert("菜單加載失敗，請稍後再試！");
        this.menu = [];
      } finally {
        this.loadingMenu = false;
      }
    },


    // 添加商品到購物車
    addToCart(item) {
      const existingItem = this.cart.find(cartItem => cartItem.id === item.id);
      if (existingItem) {
        existingItem.quantity += 1;
      } else {
        this.cart.push({ ...item, quantity: 1 });
      }
    },

    // 移除商品
    removeFromCart(index) {
      this.cart.splice(index, 1);
    },

    // 驗證信用卡
    validateCard() {
      const regex = /^[0-9]{16}$/;
      this.isCardValid = regex.test(this.creditCardNumber);
    },

    // 結帳
    async checkout() {
      if (this.cart.length === 0) {
        alert("購物車為空，請先選擇商品！");
        return;
      }

      if (this.paymentMethod === 'credit_card' && !this.isCardValid) {
        alert("信用卡號格式不正確或尚未填寫！");
        return;
      }

      this.loadingCheckout = true;
      const totalAmount = this.totalPrice;

      try {
        const response = await axios.post("http://127.0.0.1:5000/checkout", {
          cart: this.cart,
          totalPrice: totalAmount,
        });

        if (response.status === 200) {
          alert(this.paymentMethod === 'cash' ? "餐點送達請付款！" : "結帳成功！");
          this.cart = [];
        } else {
          alert("結帳失敗，請稍後再試！");
        }
      } catch (error) {
        console.error("結帳錯誤:", error);
        alert("結帳時發生錯誤，請稍後再試！");
      } finally {
        this.loadingCheckout = false;
      }
    },
  },

  mounted() {
    this.fetchRestaurants(this.maincat_selected);
  },
};
</script>


<style scoped>
.pickup {
  padding: 20px;
  background: linear-gradient(to right, #b8fcdc, #fffae3);
  border-radius: 30px;
  color: #5d4037;
}

h2, h3, h4 {
  color: #122a31;
}

select, input {
  border: 1px solid #d8d0e1;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 20px;
}

.menu-items {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.menu-item {
  display: flex;
  border: 1px solid #000000;
  border-radius: 8px;
  padding: 15px;
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(227, 179, 179, 0.1);
  transition: transform 0.2s;
}

.menu-item:hover {
  transform: scale(1.02);
}

.menu-item img {
  width: 100px;
  height: 100px;
  border-radius: 8px;
  margin-right: 15px;
}

.order-summary {
  margin-top: 20px;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #FFFFFF;
}

button {
  background-color: #1b1918;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #716b69;
}

.loading {
  color: #666;
  font-style: italic;
}
</style>
