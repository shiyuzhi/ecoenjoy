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
        <img :src="item.image" alt="菜品圖片" class="menu-image" />
        <div class="item-details">
          <h4>{{ item.name }}</h4>
          <p>{{ item.description }}</p>
          <span class="price">{{ item.price }} 元</span>
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
      <button @click="checkout" class="checkout-button">結帳</button>
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
    };
  },
  computed: {
    totalPrice() {
      return this.cart.reduce((total, item) => total + (item.price * item.quantity), 0);
    },
  },
  watch: {
    maincat_selected: {
      handler(newMaincat) {
        this.fetchRestaurants(newMaincat); // 當 maincat_selected 變化時重新加載餐廳資料
      },
      immediate: true // 初次加載時也執行
    }
  },
  methods: {
    async fetchRestaurants(maincatId) {
      if (maincatId) {
        try {
          const response = await axios.get(`http://127.0.0.1:5000/subcat/${maincatId}`);
          this.restaurants = response.data;
        } catch (error) {
          console.error("獲取餐廳資料失敗:", error);
          this.restaurants = [];
        }
      } else {
        this.restaurants = [];
      }
    },

    async fetchMenu() {
      if (this.selectedRestaurant) {
        try {
          const response = await axios.get(`http://127.0.0.1:5000/menu/${this.selectedRestaurant}`);
          this.menu = response.data;
        } catch (error) {
          console.error("無法載入菜單資料:", error);
          this.menu = [];
        }
      }
    },

    addToCart(item) {
      const existingItem = this.cart.find(cartItem => cartItem.id === item.id);
      if (existingItem) {
        existingItem.quantity += 1;
      } else {
        this.cart.push({ ...item, quantity: 1 });
      }
    },

    removeFromCart(index) {
      this.cart.splice(index, 1);
    },

    async checkout() {
      if (this.cart.length === 0) {
        alert("購物車為空，請先選擇商品！");
        return;
      }

      const totalAmount = this.totalPrice;
      try {
        const response = await axios.post("http://127.0.0.1:5000/checkout", {
          cart: this.cart,
          totalPrice: totalAmount,
        });

        if (response.status === 200) {
          alert("結帳成功！");
          this.cart = [];
        } else {
          alert("結帳失敗，請稍後再試！");
        }
      } catch (error) {
        console.error("結帳錯誤:", error);
        alert("結帳時發生錯誤，請稍後再試！");
      }
    }
  },
  mounted() {
    this.fetchRestaurants(this.maincat_selected);
  }
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
