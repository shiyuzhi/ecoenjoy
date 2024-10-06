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
        <span>{{ item.name }} - {{ item.price }} 元</span>
        <button @click="removeFromCart(index)" class="remove-button">移除</button>
      </div>
      <p class="total-price">總價: {{ totalPrice }} 元</p>
      <button @click="checkout" class="checkout-button">結帳</button>
    </div>
    <p v-else>尚未添加任何商品到購物車。</p>
  </div>
</template>

<script>
export default {
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
      return this.cart.reduce((total, item) => total + item.price, 0);
    },
  },
  methods: {
    addToCart(item) {
      this.cart.push(item);
    },
    removeFromCart(index) {
      this.cart.splice(index, 1);
    },
    fetchMenu() {
      // 根據選擇的餐廳獲取菜單 (這裡可以使用 API)
      this.menu = [
        { id: 1, name: '外送菜品 1', description: '描述 1', price: 100, image: 'image_url_1' },
        { id: 2, name: '外送菜品 2', description: '描述 2', price: 150, image: 'image_url_2' },
        // 添加更多的菜品
      ];
    },
    checkout() {
      alert('結帳功能尚未實現');
    },
  },
  mounted() {
    // 初始化餐廳資料 (這裡可以使用 API)
    this.restaurants = [
      { id: 1, name: '餐廳 A' },
      { id: 2, name: '餐廳 B' },
    ];
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
