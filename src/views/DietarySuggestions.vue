<template>
  <div class="dietary-suggestions">
    <h1>個人飲食建議</h1>

    <div class="nutrition-summary">
      <h2>您的營養攝取分析</h2>
      <ul>
        <li v-for="(value, key) in deficits" :key="key">
          <span :class="{ 'highlight-deficit': value > 0 }">
            {{ key }}: {{ value > 0 ? `缺少 ${value}` : '充足' }}
          </span>
        </li>
      </ul>
    </div>

    <div class="suggestions">
      <h2>建議食物清單</h2>
      <ul class="food-list">
        <li
          v-for="food in recommendations"
          :key="food.name"
          @click="selectFood(food)"
        >
          🍴 {{ food.name }} - {{ food.restaurant_name }}
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
        <button class="close-button" @click="closeModal">關閉</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";

export default {
  setup() {
    const deficits = ref({});
    const recommendations = ref([]);
    const selectedFood = ref(null);
    const comments = ref([]);
    const loadingComments = ref(false);
    const isModalOpen = ref(false); // 控制模態框開關

    const fetchRecommendations = async () => {
      try {
        const response = await axios.get("/api/recommendations", {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        });
        deficits.value = response.data.deficits;
        recommendations.value = response.data.recommendations;
      } catch (error) {
        console.error("Error fetching recommendations:", error);
      }
    };

    const fetchComments = async (foodId) => {
      loadingComments.value = true;
      try {
        const response = await axios.get(`/api/comments/store/${foodId}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        });
        comments.value = response.data || [];
      } catch (error) {
        console.error("Error fetching comments:", error);
        comments.value = [];
      } finally {
        loadingComments.value = false;
      }
    };

    const selectFood = (food) => {
      selectedFood.value = food;
      isModalOpen.value = true; // 打開模態框或顯示右側框
      fetchComments(food.id); // 載入該食物的評論
      console.log(food);
    };

    const closeModal = () => {
      isModalOpen.value = false; // 關閉模態框或右側框
      selectedFood.value = null;
      comments.value = [];
    };

    const likeComment = async (commentId) => {
      try {
        const response = await axios.post(
          `/api/comments/like/${commentId}`,
          {},
          {
            headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
          }
        );
        // 更新該評論的點讚數
        const comment = comments.value.find((c) => c.id === commentId);
        if (comment) comment.likes = response.data.likes;
      } catch (error) {
        console.error("Error liking comment:", error);
      }
    };

    onMounted(() => {
      fetchRecommendations();
    });

    return {
      deficits,
      recommendations,
      selectedFood,
      comments,
      loadingComments,
      isModalOpen,
      selectFood,
      closeModal,
      likeComment,
    };
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

  