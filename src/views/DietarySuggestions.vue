<template>
  <div class="dietary-suggestions">
    <h1>個人飲食建議</h1>

    <div class="nutrition-summary">
      <h2>您近三日的營養攝取分析</h2>
      <ul>
        <!-- 顯示缺少的營養數據 -->
        <li v-for="(value, key) in deficits" :key="'deficit-' + key" >
          <span class="highlight-deficit" v-if="value > 0">
            {{ key }}: 缺少 {{ value.toFixed(2) }} 克
          </span>
        </li>
        
        <!-- 顯示超過的營養數據 -->
        <li v-for="(value, key) in surplus" :key="'surplus-' + key" >
          <span class="highlight-surplus" v-if="value > 0">
            {{ key }}: 超過 {{ value.toFixed(2) }} 克
          </span>
        </li>

        <!-- 如果數據均衡 -->
        <li v-if="isBalanced.value">
          <span class="highlight-sufficient">
            營養攝取均衡，保持良好飲食習慣！
          </span>
        </li>
      </ul>
    </div>

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
        <button class="close-button" @click="closeModal">關閉</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from "vue";
import axios from "axios";

export default {
  setup() {
    const deficits = ref({});
    const surplus = ref({});
    const isBalanced = ref({ value: false }); // 是否顯示均衡訊息
    const recommendations = ref([]);
    const selectedFood = ref(null);
    const comments = ref([]);
    const loadingComments = ref(false);
    const isModalOpen = ref(false); // 控制模態框開關
    const token = ref(localStorage.getItem("token")); // 用戶 Token
    const userId = ref(null); // 用戶 ID
    const cartCount = ref(0); // 購物車數量
    const foodId = ref(null); // 假設我們有一個 foodId 變量

    // 請求推薦食物
    const fetchRecommendations = async () => {
      try {
        const response = await axios.get("/api/recommendations", {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        });
        // 如果後端返回的字段格式正確，將數據存入 deficits 和 surplus
        deficits.value = response.data.deficits || {};
        surplus.value = response.data.surplus || {};
        // 設定是否顯示「營養攝取均衡」訊息
        isBalanced.value = !Object.values(deficits).some(v => v > 0) && !Object.values(surplus).some(v => v > 0);

        recommendations.value = response.data.recommendations;
      } catch (error) {
        console.error("Error fetching recommendations:", error);
      }
    };

    // 請求食物的評論
    const fetchComments = async (foodId) => {
      loadingComments.value = true;
      try {
        const response = await axios.get(`/api/comments/store/${foodId}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        });
        console.log(response.data); // 確認返回數據
        comments.value = response.data.comments || [];
      } catch (error) {
        console.error("Error fetching comments:", error);
        comments.value = [];
      } finally {
        loadingComments.value = false;
      }
    };

    // 使用 watch 監控 foodId 的變化
    watch(
      () => foodId.value, // 監控 foodId 變化
      (newFoodId) => {
        if (newFoodId) {
          fetchComments(newFoodId); // 當 foodId 改變時載入新的評論
        }
      }
    );

    // 選擇食物並更新 foodId
    const selectFood = (food) => {
      selectedFood.value = food;
      foodId.value = food.id; // 更新 foodId
      isModalOpen.value = true; // 打開模態框或顯示右側框
      console.log(food);
    };

    // 關閉模態框
    const closeModal = () => {
      isModalOpen.value = false; // 關閉模態框或右側框
      selectedFood.value = null;
      comments.value = []; // 關閉時清空評論
      foodId.value = null; // 清除 foodId
    };

    // 添加商品到購物車
    const addToCart = (item) => {
      const cart = JSON.parse(localStorage.getItem("cart")) || [];
      const existingItem = cart.find((cartItem) => cartItem.id === item.id);
      if (existingItem) {
        existingItem.quantity += 1;
      } else {
        cart.push({ ...item, quantity: 1 });
      }
      localStorage.setItem("cart", JSON.stringify(cart));
      updateCartCount();
      alert("添加成功！");
    };

    // 更新購物車數量
    const updateCartCount = () => {
      const cart = JSON.parse(localStorage.getItem("cart")) || [];
      cartCount.value = cart.reduce((sum, item) => sum + item.quantity, 0);
    };

    // 點讚功能
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
      fetchRecommendations(); // 初始化頁面時載入推薦食物
    });

    return {
      deficits,
      surplus,
      isBalanced,
      recommendations,
      selectedFood,
      comments,
      loadingComments,
      isModalOpen,
      selectFood,
      closeModal,
      addToCart,
      updateCartCount,
      token,
      userId,
      cartCount,
      likeComment,
      foodId, // 將 foodId 暴露到模板中
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
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 8px;
  }

  .nutrition-summary ul {
    list-style: none;
    padding: 0;
  }

  .nutrition-summary li {
    margin: 8px 0;
  }
  
  .highlight-deficit {
    color: #d9534f; /* 紅色：表示缺少 */
    font-weight: bold;
  }

  .highlight-surplus {
    color: #f0ad4e; /* 橙色：表示過量 */
    font-weight: bold;
  }

  .highlight-sufficient {
    color: #5cb85c; /* 綠色：表示充足 */
    font-weight: bold;
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
    display: flex; /* 使用 Flexbox 來排列內容 */
    justify-content: space-between; /* 讓文字與按鈕分開 */
    align-items: center; /* 垂直置中對齊內容 */
  }

  .food-list li:hover {
    background-color: #d6d6d6;
  }

  .food-list li button {
    margin-left: 30px; /* 按鈕與文字之間的距離 */
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
    background: linear-gradient(135deg, #e0f7fa, #80deea, #26c6da); /* 三種顏色的漸層 */
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: background 1s ease; /* 漸變過渡效果 */
  }

  .food-details:hover {
    background: linear-gradient(135deg, #80deea, #26c6da, #00bcd4); /* 鼠標懸停時改變漸層色 */
  }

  .food-details img {
    width: 100%;
    border-radius: 8px;
    margin-top: 15px;
  }
  
  /* 右側 評論區 */
  .food-reviews {
    flex: 1;
    background: linear-gradient(135deg, #f1f8e9, #dcedc8, #a5d6a7); /* 三種顏色的漸層 */
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    overflow-y: auto;
    transition: background 1s ease; /* 漸變過渡效果 */
  }

  .food-reviews:hover {
    background: linear-gradient(135deg, #dcedc8, #a5d6a7, #66bb6a); /* 鼠標懸停時改變漸層色 */
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
    background: linear-gradient(135deg, #007bff, #66bbff, #007bff); /* 漸層背景 */
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 4px;
    cursor: pointer;
    transition: background 0.3s ease; /* 漸變過渡效果 */
  }
  
  .comment-actions button:hover {
    background: linear-gradient(135deg, #0056b3, #2196f3, #0056b3);
  }
  
</style>
  

  

  