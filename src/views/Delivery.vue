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

    <div v-if="showCommentsModal" class="comments-modal">
      <div class="modal-content">
        <h3>{{ selectedMenuItem.name }} 的評論</h3>
        <div v-if="selectedMenuItem.comments.length === 0" class="no-comments-message">
          <p>目前還沒評論喔！來第一個留言吧！</p>
        </div>
        <div v-else class="comments-container">
          <ul>
            <li v-for="(comment, index) in selectedMenuItem.comments" :key="index" class="comment-card">
              <p class="comment-user"><strong>{{ comment.user.username }}</strong>: <span class="comment-text">{{ comment.data }}</span></p>
              <div class="comment-meta"><span>👍 {{ comment.likes }} 喜歡</span> | <span>💬 {{ comment.replies }} 回覆</span></div>
            </li>
          </ul>
        </div>
        <button @click="closeCommentsModal" class="close-modal-button">關閉</button>
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
        showCommentsModal: false, // 控制評論模態框顯示
        selectedMenuItem: null, // 當前選擇的菜品
        showCommentsModal: false, // 控制評論模態框顯示
        selectedMenuItem: null, // 當前選擇的菜品
        newComment: '', // 儲存用戶新寫的評論
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
      // 查看評論
      async viewComments(item) {
        this.selectedMenuItem = { ...item, comments: [] }; // 初始化當前菜品數據

        try {
          const response = await axios.get(`http://127.0.0.1:5000/api/comments/store/${this.selectedMenuItem.id}`);
          if (response.status === 200) {
            // 如果返回的評論是空數組
            if (response.data.length === 0) {
              this.selectedMenuItem.comments = []; // 空評論
              this.noCommentsMessage = "目前還沒評論喔！來第一個留言吧！";
            } else {
              this.selectedMenuItem.comments = response.data; // 設置評論數據
              this.noCommentsMessage = ""; // 清除消息
            }
          } else {
            console.error("評論加載失敗:", response.data.message);
            this.noCommentsMessage = "無法加載評論，請稍後再試。";
          }
        } catch (error) {
          console.error("獲取評論時發生錯誤:", error.message || error);
          this.noCommentsMessage = "獲取評論時發生錯誤。";
        } finally {
          this.showCommentsModal = true; // 顯示模態框
        }
      },

      // 提交新評論
      async submitComment() {
      if (!this.isLoggedIn) {
        alert("請先登入才能提交評論！");
        return; // 用戶未登入，阻止評論提交
      }

      if (!this.newComment.trim()) {
        alert("請輸入評論內容！");
        return;
      }

    const commentData = {
      user_id: this.userId, // 用戶 ID
      menu_item_id: this.selectedMenuItem.id, // 當前菜品 ID
      comment: this.newComment, // 用戶輸入的評論內容
    };

    try {
      const response = await axios.post("http://127.0.0.1:5000/api/comments", commentData, {
        headers: { Authorization: `Bearer ${this.token}` }
      });

      if (response.status === 200) {
        this.selectedMenuItem.comments.push(response.data); // 更新菜品的評論
        this.newComment = ''; // 清空評論框
      } else {
        console.error("評論提交失敗:", response.data.message);
      }
    } catch (error) {
      console.error("提交評論時發生錯誤:", error.message || error);
    }
  },

      // 編輯評論（僅限登入用戶）
      async editComment(comment) {
        if (!this.isLoggedIn) {
          alert("請先登入才能編輯評論！");
          return; // 用戶未登入，阻止編輯
        }

        // 這裡可以加入編輯邏輯，根據需要提供編輯功能
        // 例如，彈出編輯框，並提交修改後的評論
        const editedComment = prompt("請編輯您的評論：", comment.comment);
        if (editedComment !== null && editedComment.trim() !== '') {
          try {
            const response = await axios.put(`http://127.0.0.1:5000/api/comments/${comment.id}`, {
              comment: editedComment
            }, {
              headers: { Authorization: `Bearer ${this.token}` }
            });

            if (response.status === 200) {
              comment.comment = editedComment; // 更新評論內容
            } else {
              console.error("評論編輯失敗:", response.data.message);
            }
          } catch (error) {
            console.error("編輯評論時發生錯誤:", error.message || error);
          }
        }
      },

      // 刪除評論（僅限登入用戶）
      async deleteComment(comment) {
        if (!this.isLoggedIn) {
          alert("請先登入才能刪除評論！");
          return; // 用戶未登入，阻止刪除
        }

        const confirmDelete = confirm("您確定要刪除此評論嗎？");
        if (confirmDelete) {
          try {
            const response = await axios.delete(`http://127.0.0.1:5000/api/comments/${comment.id}`, {
              headers: { Authorization: `Bearer ${this.token}` }
            });

            if (response.status === 200) {
              const index = this.selectedMenuItem.comments.findIndex(c => c.id === comment.id);
              if (index !== -1) {
                this.selectedMenuItem.comments.splice(index, 1); // 刪除評論
              }
            } else {
              console.error("評論刪除失敗:", response.data.message);
            }
          } catch (error) {
            console.error("刪除評論時發生錯誤:", error.message || error);
          }
        }
      },

      // 關閉評論模態框
      closeCommentsModal() {
        this.showCommentsModal = false;
        this.selectedMenuItem = null; // 清空選擇的菜品數據
      },
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
.comments-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.5); /* 加深背景色 */
  z-index: 1000;
}

.modal-content {
  background: #fff;
  padding: 30px;
  border-radius: 12px;
  max-width: 700px;
  width: 90%;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  animation: slideIn 0.5s ease-out;
  border-left: 5px solid #5c6bc0; /* 加入顏色條 */
}

@keyframes slideIn {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.comments-container {
  margin-top: 20px;
  max-height: 400px;
  overflow-y: auto;
  padding-right: 10px;
}

.comment-card {
  background: #f4f4f9;
  padding: 15px;
  margin-bottom: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border-left: 5px solid #ff4081; /* 加入顏色條 */
}

.comment-card:hover {
  transform: translateX(7px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  border-left: 5px solid #ff5722; /* 增加滑鼠懸停效果 */
}

.comment-user {
  font-size: 1.1rem;
  font-weight: bold;
  color: #2f3b52;
  margin-bottom: 5px;
}

.comment-text {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.5;
}

.comment-meta {
  margin-top: 10px;
  font-size: 0.85rem;
  color: #888;
}

.close-modal-button {
  background-color: #1e88e5;
  color: white;
  padding: 12px 25px;
  font-size: 1.1rem;
  border: none;
  border-radius: 50px; /* 圓形按鈕 */
  cursor: pointer;
  margin-top: 30px;
  transition: background-color 0.3s, transform 0.2s;
}

.close-modal-button:hover {
  background-color: #1565c0;
  transform: scale(1.05); /* 按鈕放大效果 */
}



</style>