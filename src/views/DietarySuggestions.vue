<template>
  <div class="dietary-suggestions">
    <h1>個人飲食建議</h1>

    <!-- 營養攝取分析 -->
    <div class="nutrition-summary">
      <h2>您近三日的營養攝取分析</h2>
      <ul>
        <li v-for="(value, key) in deficits" :key="key">
          <span :class="{ 'highlight-deficit': value > 0 }">
            {{ key }}: {{ value > 0 ? `缺少 ${value}` : '充足' }}
          </span>
        </li>
      </ul>
    </div>

    <!-- 推薦食物清單 -->
    <div class="suggestions">
      <h2>建議食物清單</h2>
      <ul class="food-list">
        <li v-for="food in recommendations" :key="food.name">
          <span @click="selectFood(food)">
            🍴 {{ food.name }} - {{ food.restaurant_name }}
          </span>
          <button @click="addToCart(food)">加入購物車</button>
        </li>
      </ul>
    </div>

    <!-- 模態框 -->
    <div v-if="isModalOpen" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <div class="details-container">
          <!-- 左側 餐點詳細資訊 -->
          <div class="food-details">
            <h2>{{ selectedFood.name }} 詳細資訊</h2>
            <p>餐廳: {{ selectedFood.restaurant_name }}</p>
            <p>碳水化合物: {{ selectedFood.carbs }} 克</p>
            <p>蛋白質: {{ selectedFood.protein }} 克</p>
            <p>脂肪: {{ selectedFood.fat }} 克</p>
            <p>熱量: {{ selectedFood.calories }} 千卡</p>
            <img :src="selectedFood.img_url" alt="Food Image" class="food-img" />
          </div>

          <!-- 右側 評論區 -->
          <div class="food-reviews">
            <h2>評論</h2>
            <div v-if="loadingComments">載入中...</div>
            <ul v-else-if="comments.length">
              <li v-for="comment in comments" :key="comment.id" class="comment-item">
                <p>{{ comment.data }}</p>
                <small>作者: {{ comment.user?.username || "匿名" }}</small>
                <div class="comment-actions">
                  <button @click="likeComment(comment.id)">👍 {{ comment.likes }}</button>
                  <span>回覆數: {{ comment.replies }}</span>
                </div>
              </li>
            </ul>
            <p v-else>暫無評論</p>
          </div>
        </div>

        <!-- 按鈕區域 -->
        <div class="modal-buttons">
          <button class="close-button" @click="closeModal">關閉</button>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import { ref, onMounted } from "vue";
import axios from "axios";

export default {
  data() {
    return {
      deficits: {}, // 營養缺失資料
      recommendations: [], // 推薦食物清單
      selectedFood: null, // 被選擇的食物
      comments: [], // 評論清單
      loadingComments: false, // 評論加載狀態
      isModalOpen: false, // 模態框開關
      isLoggedIn: !!localStorage.getItem("token"), // 是否已登入
      token: localStorage.getItem("token"), // 用戶 Token
      userId: null, // 用戶 ID
    };
  },
  
  methods: {
    // 獲取推薦食物
    async fetchRecommendations() {
      try {
        const response = await axios.get("/api/recommendations", {
          headers: { Authorization: `Bearer ${this.token}` },
        });
        this.deficits = response.data.deficits;
        this.recommendations = response.data.recommendations;
      } catch (error) {
        console.error("Error fetching recommendations:", error);
      }
    },

    // 獲取評論
    async fetchComments(foodId) {
      this.loadingComments = true;
      try {
        const response = await axios.get(`/api/comments/store/${foodId}`, {
          headers: { Authorization: `Bearer ${this.token}` },
        });
        this.comments = response.data || [];
      } catch (error) {
        console.error("Error fetching comments:", error);
        this.comments = [];
      } finally {
        this.loadingComments = false;
      }
    },

    // 選擇某個食物並打開模態框
    selectFood(food) {
      this.selectedFood = food;
      this.isModalOpen = true;
      this.fetchComments(food.id);
    },

    // 關閉模態框
    closeModal() {
      this.isModalOpen = false;
      this.selectedFood = null;
      this.comments = [];
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

    // 點讚評論
    async likeComment(commentId) {
      try {
        const response = await axios.post(
          `/api/comments/like/${commentId}`,
          {},
          {
            headers: { Authorization: `Bearer ${this.token}` },
          }
        );

        const comment = this.comments.find((c) => c.id === commentId);
        if (comment) comment.likes = response.data.likes;
      } catch (error) {
        console.error("Error liking comment:", error);
      }
    },
  },
  mounted() {
    this.fetchRecommendations();
  },
};
</script>



  
<style scoped>
.dietary-suggestions {
  padding: 20px;
  background-color: #fafafa;
  border: 3px solid #000000;
  border-radius: 10px;
  max-width: 900px;
  margin: 20px auto;
}

h1, h2 {
  color: #000000;
  text-align: center;
}

.nutrition-summary {
  margin-bottom: 20px;
}

.highlight-deficit {
  color: red;
}

.food-list {
  list-style-type: none;
  padding: 0;
}

.food-list li {
  background-color: #e9ecef;
  border-radius: 5px;
  padding: 10px;
  margin: 5px 0;
  cursor: pointer;
  transition: background-color 0.3s;
}

.food-list li:hover {
  background-color: #d6d6d6;
}

/* 模態框背景 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

/* 模態框內容 */
.modal-content {
  background: #ffffff;
  border-radius: 8px;
  padding: 20px;
  width: 80%;
  max-width: 900px;
  max-height: 90%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

/* 按鈕區域 */
.modal-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 15px;
}

/* 關閉按鈕 */
.close-button {
  margin-top: 10px;
  padding: 8px 12px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  align-self: flex-end;
}

.close-button:hover {
  background-color: #c82333;
}

.checkout-button {
  background-color: #28a745;
  color: white;
}

.checkout-button:hover {
  background-color: #218838;
}

.checkout-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

/* 主內容佈局 */
.details-container {
  display: flex;
  gap: 20px;
}

/* 左側 餐點資訊 */
.food-details {
  flex: 1;
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.food-details img {
  width: 100%;
  border-radius: 8px;
  margin-top: 15px;
}

/* 右側 評論區 */
.food-reviews {
  flex: 1;
  background: #f1f3f5;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
}

.comment-item {
  background: #ffffff;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.comment-actions {
  margin-top: 8px;
  display: flex;
  gap: 10px;
  align-items: center;
}

.comment-actions button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.comment-actions button:hover {
  background-color: #0056b3;
}
</style>

  