<template>
  <div class="store-details">
    <!-- 返回按鈕 -->
    <button @click="goBack" class="back-button">返回</button>
    <hr />
    <!-- 餐廳詳細資訊顯示 -->
    <div class="image-container">
      <img v-if="restaurant && restaurant.img_url" :src="`/store/${restaurant.img_url}`" :alt="restaurant.name" class="restaurant-image" />
    </div>
    <h2>{{ restaurant ? restaurant.name : '餐廳名稱' }}</h2>
    <p>{{ restaurant ? restaurant.address : '餐廳地址' }}</p>
    <p>{{ restaurant ? restaurant.type : '餐廳類型' }}</p>
  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    inject: ['selectedRestaurant'],
    data() {
      return {
        restaurant: null,
      };
    },
    created() {
      // 檢查是否有從父組件接收資料
      if (this.selectedRestaurant) {
        this.restaurant = this.selectedRestaurant;
      } else {
        const restaurantId = this.$route.params.id; // 獲取餐廳 ID
        if (restaurantId) {
          this.fetchRestaurantDetails(restaurantId); // 根據 ID 發送請求
        } else {
          console.error('無效的餐廳 ID');
        }
      }
    },
    methods: {
      // 獲取餐廳詳細資訊
      async fetchRestaurantDetails(id) {
        try {
          const response = await axios.get(`http://127.0.0.1:5000/api/subcat/id/${id}`);
          this.restaurant = response.data;  // 儲存餐廳資料
        } catch (error) {
          console.error('餐廳資料加載失敗', error);
        }
      },

      // 返回上一頁
      goBack() {
        this.$router.go(-1);
      }
    },

    watch: {
      // 監控路由參數，當餐廳 ID 更新時重新發送請求
      '$route.params.id': function(newId) {
        this.fetchRestaurantDetails(newId);
      }
    }
  };
</script>

<style scoped>
  .store-details {
    font-family: Arial, sans-serif;
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    background: linear-gradient(45deg, #6cc9fb, #f9feff, #fda3ec);
  }
  
  .back-button {
    background: linear-gradient(45deg, #0670e1, #27e3d4);
    color: white;
    border: none;
    padding: 12px 24px;
    font-size: 16px;
    cursor: pointer;
    border-radius: 8px;
    margin-bottom: 20px;
    transition: transform 0.3s ease, box-shadow 0.3s ease, background 0.3s ease;
  }
  
  .back-button:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    background: linear-gradient(45deg, #0056b3, #009d91);
  }
  
  .image-container {
    text-align: center;
    margin-bottom: 20px;
  }
  
  .restaurant-image {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    border: 4px solid #ddd; /* 餐廳照片的邊框 */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 增加陰影效果 */
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .restaurant-image:hover {
    transform: scale(1.05); /* 當圖片懸停時稍微放大 */
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* 改變陰影效果 */
  }
  
  h2 {
    text-align: center;
    font-size: 28px;
    margin-top: 0;
    color: #333;
  }
  
  p {
    text-align: center;
    font-size: 16px;
    color: #666;
    margin: 5px 0;
  }
</style>
