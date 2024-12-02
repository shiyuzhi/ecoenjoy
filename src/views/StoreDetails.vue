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

    <!-- 評論區 -->
    <div class="comments-section">
      <h3>評論區</h3>
      <div v-if="comments.length" class="comments-list">
        <div v-for="comment in comments" :key="comment.id" class="comment-item">
          <div class="comment-header">
            <p><strong>{{ comment.user.username }}</strong>: {{ comment.data }}</p>
            <div class="comment-actions">
              <button @click="likeComment(comment.id)">點讚 ({{ comment.likes }})</button>
              <button @click="toggleReply(comment.id)">回覆</button>
              <!-- 編輯按鈕只顯示給登入用戶 -->
              <button v-if="currentUser && comment.user === currentUser.username" @click="editComment(comment)">編輯</button>
            </div>
          </div>
          <!-- 回覆框 -->
        <div v-if="replyingTo === comment.id" class="reply-box">
          <textarea v-model="replyContent" placeholder="輸入回覆內容"></textarea>
          <button @click="submitReply(comment.id)">送出</button>
        </div>

        <!-- 顯示子評論 -->
          <div v-if="comment.replies && comment.replies.length > 0" class="replies">
            <ul>
              <li v-for="reply in comment.replies" :key="reply.id" class="reply-item">
                <p><strong>{{ reply.user ? reply.user.name : '匿名' }}</strong>: {{ reply.data }}</p>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <p v-else>目前沒有評論，歡迎新增評論！</p>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  
  export default {
    inject: ['selectedRestaurant'],
    data() {
      return {
        restaurant: null,
        comments: [],
        currentUser: null, // 預設為 null，表示訪客
        replyingTo: null,
        replyContent: '',
      };
    },
    created() {
      // 檢查是否有從父組件接收資料
      if (this.selectedRestaurant) {
        this.restaurant = this.selectedRestaurant;
        this.fetchComments(this.restaurant.id); // 使用父組件傳遞的餐廳資料
      } else {
        const restaurantId = this.$route.params.id; // 獲取餐廳 ID
        if (restaurantId) {
          this.fetchRestaurantDetails(restaurantId); // 根據 ID 發送請求
          this.fetchComments(restaurantId);
        } else {
          console.error('無效的餐廳 ID');
        }
      }
  
      // 檢查用戶登入狀態
      this.checkLoginStatus();
    },
    methods: {
      // 檢查是否已登入
      checkLoginStatus() {
        const token = localStorage.getItem('authToken'); // 假設使用 JWT 存儲登入資訊
        if (token) {
          // 假設你有一個解碼 JWT 的函式
          this.currentUser = this.decodeJWT(token);
        }
      },
  
      // 解碼 JWT 的範例
      decodeJWT(token) {
        try {
          // 假設用於解碼 token 的邏輯
          const payload = atob(token.split('.')[1]);
          return JSON.parse(payload);
        } catch (error) {
          console.error('解碼 JWT 失敗', error);
          return null;
        }
      },
  
      // 發送請求並獲取餐廳詳細資料
      async fetchRestaurantDetails(id) {
        try {
          const response = await axios.get(`http://127.0.0.1:5000/api/subcat/id/${id}`);
          this.restaurant = response.data; // 儲存餐廳資料
        } catch (error) {
          console.error('餐廳資料加載失敗', error);
        }
      },
  
      // 獲取評論資料
      async fetchComments(foodId) {
        try {
          const response = await axios.get(`http://127.0.0.1:5000/api/comments/store/${foodId}`);
          if (response.data.length === 0) {
            console.log('No comments available for this food item.');
          } else {
            this.comments = response.data;
          }
        } catch (error) {
          console.error('無法加載評論', error);
          if (error.response && error.response.status === 404) {
            alert("這道菜品目前沒有評論！");
          } 
        }
      },

  
      // 點讚評論
      async likeComment(commentId) {
        try {
          const token = localStorage.getItem('token');  // 假設 JWT 存儲在 localStorage 中
          const response = await axios.post(`http://127.0.0.1:5000/api/comments/like/${commentId}`,
            {},
            {
              headers: {
                Authorization: `Bearer ${token}`  // 設置 Authorization 標頭
              }
            }
          );
          const updatedComment = this.comments.find(comment => comment.id === commentId);
          if (updatedComment) {
            updatedComment.likes = response.data.likes;
          }
        } catch (error) {
          console.error('點讚失敗', error);
        }
      },

      
      
      // 切換回覆框顯示
      toggleReply(commentId) {
        this.replyingTo = this.replyingTo === commentId ? null : commentId;
        this.replyContent = '';  // 清空輸入框
      },
  
      // 發送回覆
      async submitReply(parentCommentId) {
        if (!this.replyContent.trim()) {
          alert("回覆內容不能為空！");
          return;
        }
        try {
          const token = localStorage.getItem('token');  // 假設 JWT 存儲在 localStorage 中
          const response = await axios.post(`http://127.0.0.1:5000/api/comments/reply/${parentCommentId})`,
            {},
            {
              headers: {
                Authorization: `Bearer ${token}`  // 設置 Authorization 標頭
              }
            }
          );

          // 處理回覆成功邏輯
          if (response.status === 201) {
            alert("回覆成功！");
            // 可以清空回覆內容或執行其他操作
            this.replyContent = '';  // 清空回覆內容框
            this.replyingTo = null;   // 隱藏回覆框
          } else {
            alert("回覆發生錯誤，請稍後再試！");
          }
        } catch (error) {
          console.error("回覆失敗:", error);
          alert("回覆失敗，請稍後再試！");
        }
      },

      // 編輯評論
      async editComment(comment) {
        const newContent = prompt('編輯你的評論：', comment.data);
        if (newContent && newContent !== comment.data) {
          try {
            await axios.put(`http://127.0.0.1:5000/api/comments/${comment.id}`, {
              data: newContent,
            });
            comment.data = newContent;
          } catch (error) {
            console.error('編輯評論失敗', error);
          }
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
        this.fetchComments(newId);
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
  
  .comments-section {
    background-color: #fff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  .comments-section h3 {
    font-size: 24px;
    color: #333;
    margin-bottom: 15px;
  }
  
  .comments-list {
    margin-top: 20px;
  }
  
  .comment-item {
    background-color: #f7f7f7;
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 15px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease, background-color 0.2s ease;
  }
  
  .comment-item:hover {
    transform: translateY(-5px);
    background-color: #f1f1f1;
  }
  
  .comment-header p {
    font-size: 16px;
    color: #333;
  }
  
  .comment-actions {
    margin-top: 10px;
  }
  
  .comment-actions button {
    background: linear-gradient(45deg, #a8d4ff, #4aff96);
    color: rgb(1, 1, 1);
    border: none;
    padding: 8px 16px;
    font-size: 14px;
    cursor: pointer;
    border-radius: 5px;
    margin-right: 8px;
    transition: transform 0.3s ease, box-shadow 0.3s ease, background 0.3s ease;
  }
  
  .comment-actions button:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
    background: linear-gradient(45deg, #c4d8ee, #ffa9e8);
  }
  
  .reply-box {
    margin-top: 10px;
    display: flex;
    flex-direction: column;
  }
  
  .reply-box textarea {
    width: 100%;
    padding: 10px;
    font-size: 14px;
    border-radius: 8px;
    border: 1px solid #ddd;
    resize: none;
    margin-bottom: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    transition: border-color 0.3s ease;
  }
  
  .reply-box textarea:focus {
    border-color: #007bff;
  }
  
  .reply-box button {
    background-color: #007bff;
    color: white;
    padding: 10px;
    font-size: 14px;
    border-radius: 5px;
    cursor: pointer;
    transition: transform 0.3s ease, background-color 0.3s ease;
  }
  
  .reply-box button:hover {
    background-color: #0056b3;
    transform: translateY(-3px);
  }
  
  .replies {
    margin-top: 20px;
    padding-left: 20px;
  }
  
  .reply-item {
    background-color: #f1f1f1;
    border-radius: 5px;
    padding: 8px;
    margin-bottom: 10px;
    font-size: 14px;
  }
  
  .reply-item p {
    margin: 0;
  }
  
  .reply-item strong {
    color: #007bff;
  }
</style>
  