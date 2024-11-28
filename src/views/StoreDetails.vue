<template>
    <div class="store-details">
      <!-- 返回按鈕 -->
      <button @click="$router.back()" class="back-button">返回</button>
  
      <!-- 餐廳資訊 -->
      <div v-if="restaurant">
        <h2>{{ restaurant.name }}</h2>
        <p>地址: {{ restaurant.address }}</p>
        <p>類型: {{ restaurant.type }}</p>
      </div>
      <p v-else>正在加載餐廳資料...</p>
  
      <!-- 評論列表 -->
      <div v-if="comments.length">
        <h3>評論</h3>
        <ul class="comment-list">
          <li v-for="comment in comments" :key="comment.id" class="comment-item">
            <p><strong>{{ comment.user }}</strong>: {{ comment.data }}</p>
            <div class="comment-actions">
              <span>讚: {{ comment.likes }}</span>
              <button @click="likeComment(comment.id)" class="like-button">點讚</button>
            </div>
          </li>
        </ul>
      </div>
      <p v-else-if="restaurant">尚無評論</p>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    name: "StoreDetails",
    props: {
      id: {
        type: String,
        required: true,
      },
    },
    data() {
      return {
        restaurant: null, // 餐廳資料
        comments: [], // 評論資料
      };
    },
    methods: {
      // 獲取餐廳詳細資訊與評論
      async fetchDetails() {
        try {
          // 獲取餐廳詳細資料
          const restaurantResponse = await axios.get(`/subcat/${this.id}`);
          this.restaurant = restaurantResponse.data;
  
          // 獲取餐廳的評論
          const commentsResponse = await axios.get(`/comments/${this.id}`);
          this.comments = commentsResponse.data;
        } catch (error) {
          console.error("加載資料失敗:", error);
        }
      },
      // 點讚功能
      async likeComment(commentId) {
        try {
          await axios.post(`/comments/like/${commentId}`);
          const comment = this.comments.find((c) => c.id === commentId);
          if (comment) comment.likes++;
        } catch (error) {
          console.error("點讚失敗:", error);
        }
      },
    },
    watch: {
      // 當 ID 改變時重新加載資料
      id() {
        this.fetchDetails();
      },
    },
    mounted() {
      this.fetchDetails(); // 初次加載時獲取資料
    },
  };
  </script>
  
  <style scoped>
  .store-details {
    padding: 20px;
    font-family: Arial, sans-serif;
  }
  
  .back-button {
    background-color: #007bff;
    color: #fff;
    border: none;
    padding: 10px 15px;
    margin-bottom: 15px;
    cursor: pointer;
    border-radius: 5px;
  }
  
  .back-button:hover {
    background-color: #0056b3;
  }
  
  .comment-list {
    list-style-type: none;
    padding: 0;
  }
  
  .comment-item {
    border-bottom: 1px solid #ddd;
    margin-bottom: 10px;
    padding-bottom: 10px;
  }
  
  .comment-actions {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .like-button {
    background-color: #28a745;
    color: #fff;
    border: none;
    padding: 5px 10px;
    cursor: pointer;
    border-radius: 5px;
  }
  
  .like-button:hover {
    background-color: #218838;
  }
</style>
  