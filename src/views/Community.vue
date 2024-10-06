<template>
  <div class="community">
    <h2>社群空間</h2>
    <div class="comments">
      <h3>用戶評論</h3>
      <div class="comment" v-for="comment in comments" :key="comment.id">
        <strong>{{ comment.username }}:</strong>
        <p>{{ comment.text }}</p>
        <button @click="editComment(comment)">編輯</button>
        <button @click="deleteComment(comment.id)">刪除</button>
      </div>
    </div>
    
    <div class="new-comment">
      <textarea v-model="newComment" placeholder="撰寫評論..."></textarea>
      <button @click="submitComment">提交評論</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      comments: [
        { id: 1, username: '用戶 A', text: '這個餐廳的外送很好！' },
        { id: 2, username: '用戶 B', text: '自取服務也很快速！' },
      ],
      newComment: '',
    };
  },
  methods: {
    submitComment() {
      if (this.newComment.trim()) {
        this.comments.push({
          id: this.comments.length + 1,
          username: '新用戶',
          text: this.newComment,
        });
        this.newComment = '';
      } else {
        alert('請輸入評論內容');
      }
    },
    editComment(comment) {
      const editedText = prompt("編輯評論", comment.text);
      if (editedText !== null && editedText.trim()) {
        comment.text = editedText; //更新
      }
    },
    deleteComment(commentId) {
      this.comments = this.comments.filter(comment => comment.id !== commentId); // 刪除評論
    },
  },
};
</script>

<style scoped>
.community {
  padding: 20px;
  background: linear-gradient(to right, #68cfff, #ff72a6); /* 淺藍色到淺橙色的漸變背景 */
  border-radius: 5px; 
  color: #333; 
}

.comments {
  margin-bottom: 20px;
  padding: 15px;
  background: white; 
  border: 1px solid #ddd; 
  border-radius: 50px; 
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); 
}

.comment {
  margin-bottom: 20px;
}

.new-comment {
  display: flex;
  flex-direction: column;
  background: #fff; 
  border: 1px solid #ddd; 
  border-radius: 10px; 
  padding: 15px; 
}

.new-comment textarea {
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px; 
  padding: 10px; 
  resize: none; 
}

.new-comment button {
  background-color: #192f38; 
  color: white; 
  border: none; 
  border-radius: 5px; 
  padding: 10px; 
  cursor: pointer; 
}

.new-comment button:hover {
  background-color: #3d3841; 
}
</style>
