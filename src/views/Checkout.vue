<template>
    <div class="checkout-page">
      <h1>結帳頁面</h1>
      <div class="order-summary">
        <h3>訂單總覽</h3>
        <div v-for="(item, index) in cart" :key="index" class="cart-item">
          <span>{{ item.name }} - {{ item.quantity }} x {{ item.price }} 元</span>
        </div>
        <p class="total-price">總價: {{ totalPrice }} 元</p>
        <button v-if="cart.length" @click="clearCart" class="clear-cart-button">清空訂單</button>
      </div>
  
      <h4>送餐資訊</h4>
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
/* 訂單總覽樣式 */
.order-summary {
  background-color: #fff;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: 20px auto;
}
.cart-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 0.95rem;
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
.clear-cart-button {
  margin-top: 10px;
  background-color: red;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
}

.clear-cart-button:hover {
  background-color: darkred;
}
</style>