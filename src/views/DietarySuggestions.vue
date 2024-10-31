<template>
    <div class="dietary-suggestions">
      <h1>個人飲食建議</h1>
      
      <div class="suggestions">
        <h2>建議食物清單</h2>
        <ul class="food-list">
          <li>🍎 蘋果 - 含豐富纖維和維他命C</li>
          <li>🥦 綠花椰菜 - 有助於抗氧化</li>
          <li>🐟 三文魚 - 優質蛋白和Omega-3脂肪酸</li>
          <li>🍗 雞胸肉 - 低脂高蛋白的良好來源</li>
          <li>🥑 酪梨 - 健康的脂肪來源</li>
        </ul>
      </div>
  
      <div class="tips">
        <h2>飲食小提示</h2>
        <p>保持均衡的飲食，確保攝取多種食物以獲得足夠的營養。</p>
        <p>多喝水，每天至少10杯，保持身體水分充足。</p>
      </div>
  
      <div class="user-input">
        <h2>您的飲食偏好</h2>
        <textarea v-model="userPreference" placeholder="在此輸入您的飲食偏好或需求..."></textarea>
        <button @click="submitPreference" class="submit-button">提交</button>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  
  export default {
    setup() {
      const userPreference = ref('');
  
      const submitPreference = () => {
        // 這裡可以添加提交偏好的邏輯，例如發送到伺服器
        alert(`您的偏好已提交: ${userPreference.value}`);
        userPreference.value = ''; // 提交後清空輸入框
      };
  
      return {
        userPreference,
        submitPreference,
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
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    max-width: 600px;
    margin: 20px auto;
  }
  
  h1 {
    color: #000000;
    text-align: center;
    margin-bottom: 20px;
  }
  
  .suggestions, .tips, .user-input {
    margin-bottom: 20px;
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
  }
  
  .user-input textarea {
    width: 80%;
    height: 80px;
    border: 1px solid #ffd3d3;
    border-radius: 5px;
    padding: 10px;
    margin-bottom: 10px;
    font-size: 16px;
  }
  
  .submit-button {
    padding: 10px 15px;
    background-color: #28a745;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
    display: block;
    width: 100%;
  }
  
  .submit-button:hover {
    background-color: #218838;
  }
  </style>
  