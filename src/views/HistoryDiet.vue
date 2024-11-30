<template>
    <div class="history-diet">
      <h1>歷史訂單</h1>
  
      <!-- 營養總和 -->
      <div class="nutrition-summary" v-if="totals">
        <h2>今日營養總和</h2>
        <p>碳水化合物：{{ totals.carbo }} g</p>
        <p>蛋白質：{{ totals.protein }} g</p>
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
  }
  
  .nutrition-summary {
    margin-bottom: 20px;
    background: #f5f5f5;
    padding: 15px;
    border-radius: 8px;
  }
  
  .order-cards {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
  }
  
  .order-card {
    display: flex;
    align-items: center;
    border: 1px solid #ddd;
    padding: 10px;
    border-radius: 8px;
    width: 100%;
    max-width: 400px;
    background: #fff;
  }
  
  .food-image {
    width: 80px;
    height: 80px;
    object-fit: cover;
    border-radius: 8px;
    margin-right: 15px;
  }
  
  .order-details {
    flex: 1;
  }
  
  .order-price {
    font-weight: bold;
    font-size: 18px;
  }
  </style>