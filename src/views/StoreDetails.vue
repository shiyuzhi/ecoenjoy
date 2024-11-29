<template>
  <div class="store-details">
    <button @click="goBack" class="back-button">返回</button>
    <h2>{{ restaurant ? restaurant.name : '餐廳名稱' }}</h2>
    <p>{{ restaurant ? restaurant.address : '餐廳地址' }}</p>
    <p>{{ restaurant ? restaurant.type : '餐廳類型' }}</p>
  </div>
</template>

<script>
  import axios from 'axios';
  
  export default {
    inject: ['selectedRestaurant'],  // 從父組件注入 selectedRestaurant
    data() {
      return {
        restaurant: null,  // 儲存餐廳詳細資料
      };
    },
    created() {
      // 優先檢查 selectedRestaurant 是否已經傳遞過來
      if (this.selectedRestaurant) {
        this.restaurant = this.selectedRestaurant;  // 使用父組件傳遞的資料
        console.log("從父組件接收到餐廳資料:", this.restaurant);  // 輸出確認
      } else {
        const restaurantId = this.$route.params.id;  // 獲取餐廳 ID
        console.log('Restaurant ID:', restaurantId);  // 輸出 ID，確認是否正確
        if (restaurantId) {
          this.fetchRestaurantDetails(restaurantId);  // 根據 ID 發送請求
        } else {
          console.error('無效的餐廳 ID');
        }
      }
    },
    methods: {
      // 發送請求並獲取餐廳詳細資料
      async fetchRestaurantDetails(id) {
        console.log("發送請求的餐廳 ID:", id);  // 顯示請求的 ID
        try {
          const response = await axios.get(`http://127.0.0.1:5000/api/subcat/id/${id}`);  // 使用 ID 查詢
          console.log("收到的餐廳資料:", response.data);  // 輸出回應資料
          this.restaurant = response.data;  // 儲存餐廳資料
        } catch (error) {
          console.error("餐廳資料加載失敗", error);  // 顯示錯誤訊息
        }
      },
      // 返回上一頁
      goBack() {
        this.$router.go(-1);  // 返回上一頁
      },
    },
    watch: {
      // 監控 ID 更新，重新發送請求
      '$route.params.id': function(newId) {
        console.log("路由 ID 更新為:", newId);
        this.fetchRestaurantDetails(newId);  // 重新發送請求
      }
    }
  };
</script>

