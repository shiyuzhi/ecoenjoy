<template>
  <div class="food-forum">
    <h2>飲食討論區</h2>
    <div class="food-item" v-for="food in foodItems" :key="food.id">
      <div class="food-header">
        <img :src="food.image" alt="food" class="food-image"/>
        <div class="food-text">
          <h3>{{ food.name }}</h3>
        </div>
      </div>
      <div class="comments">
        <h2>評論</h2>
        <div class="comment" v-for="comment in food.comments" :key="comment.id">
          <strong>{{ comment.username }}:</strong>
          <p>{{ comment.text }}</p>
          <button @click="editComment(food.id, comment)">編輯</button>
          <button @click="deleteComment(food.id, comment.id)">刪除</button>
        </div>
      </div>

      <div class="new-comment">
        <textarea v-model="newComment[food.id]" placeholder="撰寫評論..."></textarea>
        <button @click="submitComment(food.id)">提交評論</button>
      </div>
    </div>
  </div>
</template>

<script>
  import CHICKEN from '@/assets/CHICKEN.jpg';
  import PIZZA from '@/assets/PIZZA.jpg';

  export default {
  data() {
    return {
      foodItems: [
        { 
          id: 1, 
          name: '炸雞', 
          image:  CHICKEN,
          comments: [
            { id: 1, username: 'A', text: '這個炸雞真好吃！' },
            { id: 2, username: 'B', text: '外脆內嫩，讚！' }
          ]
        },
        { 
          id: 2, 
          name: '披薩', 
          image: PIZZA,
          comments: [
            { id: 1, username: 'APPLE', text: '這家披薩的起司很濃郁！' }
          ]
        }
      ],
      newComment: {},
    };
  },
  methods: {
    submitComment(foodId) {
      const commentText = this.newComment[foodId]?.trim();
      if (commentText) {
        const food = this.foodItems.find(f => f.id === foodId);
        food.comments.push({
          id: food.comments.length + 1,
          username: '新用戶',
          text: commentText,
        });
        this.newComment[foodId] = ''; 
      } else {
        alert('請輸入評論內容');
      }
    },
    editComment(foodId, comment) {
      const editedText = prompt("編輯評論", comment.text);
      if (editedText !== null && editedText.trim()) {
        comment.text = editedText; // 更新評論內容
      }
    },
    deleteComment(foodId, commentId) {
      const food = this.foodItems.find(f => f.id === foodId);
      food.comments = food.comments.filter(comment => comment.id !== commentId); 
    },
  },
};
</script>

<style scoped>
.food-forum {
  padding: 20px;
  background: linear-gradient(to right, #ec91e2, #5b97c5); /* 漸變背景 */
  border-radius: 5px; 
  color: #333;
}

.food-item {
  margin-bottom: 30px;
  padding: 15px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.food-header {
  display: flex;
  justify-content: flex-start; 
  align-items: center; 
  margin-bottom: 15px;
}

.food-text {
  flex-grow: 1; 
}

.food-image {
  width: 200px; 
  height: 100px; 
  border-radius: 10px;
  margin-right: 20px; 
}

.food-header h3 {
  font-size: 1.5rem;
  text-align: left; /* 讓文字對齊左邊 */
}

.comments {
  margin-bottom: 20px;
}

.comments {
  margin-bottom: 20px;
  text-align: left; 
}

.comment {
  margin-bottom: 20px;
  text-align: left; 
}

.new-comment {
  display: flex;
  flex-direction: column;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 20px;
  text-align: left; 
}
</style>
