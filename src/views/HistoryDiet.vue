<template>
  <div class="history-diet">
    <h1>歷史訂單</h1>

    <!-- 營養總和 -->
    <div class="nutrition-summary" v-if="totals">
      <h2>近三日營養總和</h2>
      <p>碳水化合物：{{ Math.round(totals.carbo) }} g</p>
      <p>蛋白質：{{ Math.round(totals.protein) }} g</p>
      <p>脂肪：{{ totals.fat }} g</p>
      <p>熱量：{{ totals.calories }} kcal</p>
    </div>

    <!-- 訂單卡片 -->
    <div class="order-cards" v-if="history && history.length">
      <div v-for="(record, index) in history" :key="index" class="order-card">
        <img :src="record.img_url" alt="餐點圖片" class="food-image" />
        <div class="order-details">
          <h3>{{ record.food_name }}</h3>
          <p>餐廳：{{ record.restaurant_name }}</p>
          <p>時間：{{ new Date(record.timestamp).toLocaleString() }}</p>
        </div>
        <div class="order-price">
          <p>{{ record.price }} 元</p>
        </div>
      </div>
    </div>

    <p v-else>今天尚無訂單記錄。</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      history: [],
      totals: {},
    };
  },

  async mounted() {
    const token = localStorage.getItem("token");
    console.log("Token from localStorage: ", token);  // 調試，檢查 token 是否正確讀取

    if (!token) {
      alert("請先登入以查看歷史訂單");
      this.$router.push("/login");
      return;
    }

    try {
      const response = await axios.get("http://127.0.0.1:5000/history", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      // 檢查 API 回應的資料
      console.log("API response:", response.data); // 檢查返回資料
      if (response.status === 200 && response.data.history) {
        this.totals = response.data.totals;
        this.history = response.data.history;
      } else {
        console.error("獲取歷史訂單失敗：", response.data.message);
      }
    } catch (error) {
      if (error.response && error.response.status === 401) {
        // Token 過期，提示用戶重新登入
        alert("您的 token 已過期，請重新登入");
        this.$router.push("/login");
      } else {
        console.error("獲取歷史訂單過程中發生錯誤：", error);
      }
    }
  },
};
</script>


<style scoped>
  .history-diet {
    padding: 20px;
    background-color: #e44a4a; 
    border-radius: 10px;
  }
  
  .nutrition-summary {
    margin-bottom: 20px;
    background: #ffffff;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  .order-cards {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: space-between;
  }
  
  .order-card {
    display: flex;
    align-items: center;
    border: none;
    padding: 15px;
    border-radius: 12px;
    width: 100%;
    max-width: 350px;
    background: #ffffff;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .order-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
  }
  
  .food-image {
    width: 90px;
    height: 90px;
    object-fit: cover;
    border-radius: 10px;
    margin-right: 20px;
    border: 2px solid #ddd;
  }
  
  .order-details {
    flex: 1;
  }
  
  .order-price {
    font-weight: bold;
    font-size: 20px;  
    color: #2c3e50;
  }
  
  .order-price span {
    font-size: 30px;  /* 增加字體大小 */
    color: #27ae60;
  }
  
  /* 增加下面部分的字體大小 */
  .order-details p {
    font-size: 16px;  /* 可以視情況調整 */
    color: #333;
  }
  
  .order-details p span {
    font-size: 18px; 
    color: #7f8c8d;
  }
</style>
  