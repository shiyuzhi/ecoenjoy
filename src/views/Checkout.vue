<template>
    <div class="checkout-page">
      <h1>結帳頁面</h1>
      <div class="order-summary">
        <h3>訂單總覽</h3>
        <div v-for="(item, index) in cart" :key="index" class="cart-item">
          <span>{{ item.name }} - {{ item.quantity }} x {{ Math.round(item.price) }}  元</span>
        </div>
        <p class="total-price">總價: {{ totalPrice }} 元</p>
        <button v-if="cart.length" @click="clearCart" class="clear-cart-button">清空訂單</button>
      </div>
  
      <h4>送餐資訊</h4>
        <div class="delivery-info-container">
          <div class="form-group">
            <label for="delivery-name">取餐人姓名：</label>
            <input type="text" id="delivery-name" v-model="deliveryName" placeholder="輸入姓名" required />
          </div>
          <div class="form-group">
            <label for="delivery-address">外送地址：</label>
            <input type="text" id="delivery-address" v-model="deliveryAddress" placeholder="輸入外送地址" required />
          </div>
          <div class="form-group">
            <label for="delivery-phone">電話：</label>
            <input type="text" id="delivery-phone" v-model="deliveryPhone" placeholder="輸入電話" required />
          </div>

          <div class="payment-method">
            <button @click="paymentMethod = 'cash'" :class="{ 'active': paymentMethod === 'cash' }">現金</button>
            <button @click="paymentMethod = 'credit_card'" :class="{ 'active': paymentMethod === 'credit_card' }">信用卡</button>
          </div>
          <div v-if="paymentMethod === 'credit_card'" class="form-group">
            <label for="credit-card-number">信用卡號：</label>
            <input type="text" id="credit-card-number" v-model="creditCardNumber" placeholder="輸入信用卡號" />
            <span v-if="!isCardValid" class="error-message">信用卡號格式不正確</span>
          </div>
          <button @click="checkout" :disabled="isCheckoutDisabled" class="checkout-button">確認結帳</button>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      cart: JSON.parse(localStorage.getItem("cart")) || [],
      creditCardNumber: "",
      isCardValid: true,
      paymentMethod: "cash",
      deliveryName: "",
      deliveryAddress: "",
      deliveryPhone: "",
      isLoggedIn: !!localStorage.getItem("token"), // 是否已登入
      token: localStorage.getItem("token"), // 用戶 Token
      userId: localStorage.getItem("id"), // 用戶 ID
    };
  },
  computed: {
    totalPrice() {
      return this.cart.reduce((total, item) => total + item.price * item.quantity, 0);
    },
    isCheckoutDisabled() {
      if (this.paymentMethod === "credit_card") {
        return !this.isCardValid || !this.creditCardNumber;
      }
      return this.cart.length === 0;
    },
  },
  methods: {
    validateCard() {
      const regex = /^[0-9]{16}$/;
      this.isCardValid = regex.test(this.creditCardNumber);
    },
    async checkout() {
        if (!this.cart.length) {
          alert("購物車為空，無法結帳");
          return;
        }
        console.log('login response:', this.isLoggedIn);
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
            localStorage.setItem("cart", JSON.stringify(this.cart));
          } else {
            alert("結帳失敗：" + (response.data.error || "未知錯誤"));
          }
        } catch (error) {
          console.error("結帳過程中發生錯誤：", error.response?.data || error.message);
          alert("結帳過程中發生錯誤，請稍後再試。");
        }
    },
    // 清空購物車
    clearCart() {
      if (confirm("確定要清空訂單嗎？")) {
        this.cart = [];
        localStorage.setItem("cart", JSON.stringify(this.cart));
      }
    },
  },
  mounted() {
    if (!this.paymentMethod) {
        this.paymentMethod = 'cash';
    }
  },
};
</script>

<style>
.order-summary {
  background-color: #f7faff;
  padding: 25px;
  border-radius: 16px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  border: 2px solid #4caea9;
  max-width: 900px;
  margin: 30px auto;
  transition: box-shadow 0.3s ease, transform 0.2s ease, background-color 0.3s ease;
}

h1 {
  color: black;  /* 設置標題文字顏色為黑色 */
  font-size: 2rem;  /* 可根據需要調整標題的字型大小 */
  font-weight: bold;  /* 可選，設置為粗體字 */
  margin-bottom: 20px;  /* 可選，設定標題下方的間距 */
}

.order-summary:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
}

.cart-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  font-size: 1rem;
  padding: 10px;
  background-color: #f1f1f1;
  border-radius: 10px;
  transition: background-color 0.2s ease;
}

.cart-item:nth-child(even) {
  background-color: #e9f5f3;
}

.cart-item:hover {
  background-color: #e0f0f0;
}

.cart-item .item-name {
  font-weight: 600;
  color: #333;
}

.cart-item .item-price {
  font-weight: bold;
  color: #4caea9;
}

.total-price {
  font-size: 1.3rem;
  font-weight: bold;
  text-align: center;
  margin: 25px 0;
  color: #333;
}

h4 {
  color: black;  
  font-size: 1.5rem;  
  font-weight: bold; 
  margin-bottom: 25px;  
}


.delivery-info-container {
  background: linear-gradient(to right, #f0e3e3, #efd8d8, #d3fae1);/* 背景顏色 */
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: 30px auto;
  transition: box-shadow 0.3s ease, transform 0.2s ease;
}



.form-group {
  margin-top: 30px;
  max-width: 800px; 
  margin: 0 auto; 
}

.form-group label {
  margin-top: 30px;
  font-size: 1rem;
  margin-bottom: 10px;
  font-weight: 600;
  color: #333;
  display: block;  
  text-align: left;
  margin-left: 15px;  
}

/* 輸入框樣式 */
.form-group input {
  padding: 14px;
  font-size: 1rem;
  border: 2px solid #ccc;
  border-radius: 12px;
  width: 100%;
  transition: border-color 0.3s ease;
  box-sizing: border-box;  
}


.form-group input:focus {
  border-color: #4caea9;
  outline: none;
  box-shadow: 0 0 5px rgba(76, 174, 169, 0.4);
}

/* 付款方式選擇 */
.payment-method {
  margin-top: 25px;
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  gap: 25px;
}

.payment-method button {
  padding: 18px 36px;
  font-size: 1.2rem;
  color: #fff;
  background-color: #4caea9;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: transform 0.3s ease, background-color 0.3s ease;
}



.payment-method button.active {
  background-color: #3cada1;
  transform: scale(1.1);
}

.payment-method button:hover {
  background-color: #083b35;
  transform: scale(1.05);
}

/* error message */
.error-message {
  color: #361610;
  font-size: 0.9rem;
  margin-top: 5px;
  font-weight: 600;
}

/* 結帳按鈕 */
.checkout-button {
  background: linear-gradient(to right, #e8ffe8, #3ec8c1);
  color: rgb(22, 12, 12);
  border: none;
  padding: 14px;
  font-size: 1.2rem;
  border-radius: 12px;
  width: 100%;
  margin-top: 30px;
  cursor: pointer;
  text-align: center;
  transition: background-color 0.3s, transform 0.3s ease, box-shadow 0.2s ease;
}

.checkout-button:disabled {
  background-color: #ffd2d2;
  cursor: not-allowed;
}

.checkout-button:hover {
  background-color: #15b6e8;
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* 清空購物車按鈕 */
.clear-cart-button {
  margin-top: 25px;
  background-color: #0f0403;
  color: white;
  border: none;
  padding: 14px 24px;
  border-radius: 12px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s ease;
}

.clear-cart-button:hover {
  background-color: #d32f2f;
  transform: scale(1.05);
}

.clear-cart-button:active {
  transform: scale(1.02);
}
</style>