<template>
  <div class="pickup">
    <h2>自取</h2>
    <select v-model="selectedRestaurant" @change="fetchMenu">
      <option disabled value="">選擇餐廳</option>
      <option v-for="restaurant in restaurants" :key="restaurant.id" :value="restaurant.name">
        {{ restaurant.name }}
      </option>
    </select>

    <div class="menu-items">
      <h3>菜單</h3>
      <div class="menu-item" v-for="item in menu" :key="item.id">
        <img :src="item.image" alt="菜品圖片" />
        <div>
          <h4>{{ item.name }}</h4>
          <p>{{ item.description }}</p>
          <span>{{ item.price }} 元     </span>
          <p></p>
          <button @click="addToCart(item)">加入購物車</button>
        </div>
      </div>
    </div>

    <div class="pickup-time">
      <label for="pickup-time">選擇自取時間:</label>
      <input type="datetime-local" id="pickup-time" v-model="pickupTime" />
    </div>

    <div class="order-summary">
      <h3>訂單總覽</h3>
      <p v-for="(item, index) in cart" :key="index">
        {{ item.name }} - {{ item.price }} 元
        <button @click="removeFromCart(index)">移除</button>
      </p>
      <p>總價: {{ totalPrice }} 元</p>
      <button @click="checkout">結帳</button>
    </div>
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
      pickupTime: '',
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
      alert(`${item.name} 已加入購物車！`);
    },
    removeFromCart(index) {
      this.cart.splice(index, 1);
    },
    fetchMenu() {
      // 根據選擇的餐廳獲取菜單 (可以使用 API)
      this.menu = [
        { id: 1, name: '自取菜品 1', description: '描述 1', price: 100, image: 'image_url_1' },
        { id: 2, name: '自取菜品 2', description: '描述 2', price: 150, image: 'image_url_2' },
      ];
    },
    checkout() {
      alert('結帳功能尚未實現');
    },
  },
  mounted() {
    // 餐廳資料 (這裡可以使用 API)
    this.restaurants = [
      { id: 1, name: '餐廳 A' },
      { id: 2, name: '餐廳 B' },
      { id: 3, name: '餐廳 c' },
    ];
  },
};
</script>

<style scoped>
.pickup {
  padding: 20px;
  background: linear-gradient(to right, #b8fcdc, #fffae3); /* 淺奶油色到淡黃色漸變背景 */
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
</style>
