<template>
    <div class="profile">
      <h2>會員資料</h2>
      
      <div v-if="!isEditing">
        <p><strong>姓名:</strong> {{ userData.name }}</p>
        <p><strong>電子郵件:</strong> {{ userData.email }}</p>
        <button @click="enableEdit">編輯</button>
      </div>
      
      <div v-else>
        <label for="name">姓名</label>
        <input id="name" v-model="editedData.name" />
        
        <label for="email">電子郵件</label>
        <input id="email" v-model="editedData.email" />
        
        <button @click="saveChanges">保存</button>
        <button @click="cancelEdit">取消</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        isEditing: false,
        userData: {
          name: "John Doe",
          email: "john@example.com"
        },
        editedData: {}
      };
    },
    methods: {
      enableEdit() {
        this.isEditing = true;
        this.editedData = { ...this.userData }; // 複製現有資料
      },
      cancelEdit() {
        this.isEditing = false;
        this.editedData = {};
      },
      saveChanges() {
        this.userData = { ...this.editedData }; // 更新資料
        this.isEditing = false;
      }
    }
  };
  </script>
  
  <style scoped>
  .profile {
    padding: 20px;
  }
  label {
    display: block;
    margin: 10px 0 5px;
  }
  input {
    padding: 8px;
    width: 100%;
    margin-bottom: 15px;
  }
  button {
    margin-right: 10px;
  }
</style>
  