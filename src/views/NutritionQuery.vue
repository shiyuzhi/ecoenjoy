<template>
    <!-- 營養查詢區域 -->
    <div class="nutrition-query-container">
      <h1 class="nutrition-title">營養需求</h1>
  
      <!-- 營養素選擇區域 -->
      <div>
        <div class="nutrition-field" v-for="nutrient in nutrients" :key="nutrient.key">
          <label>{{ nutrient.label }}:</label>
          <button 
            @click="selectNutrient(nutrient.key, 'high')" 
            :class="{'selected': selectedNutrients[nutrient.key] === 'high'}">高</button>
          <button 
            @click="selectNutrient(nutrient.key, 'low')" 
            :class="{'selected': selectedNutrients[nutrient.key] === 'low'}">低</button>
        </div>
  
        <!-- 查詢按鈕 -->
        <button @click="fetchFoods" class="query-button">查詢</button>
        <!-- 重置按鈕 -->
        <button @click="resetSelections" class="reset-button">重置</button>
      </div>
  
      <!-- 查詢結果區域 -->
      <div class="query-results" v-if="queryResults.length > 0">
        <h4>推薦結果:</h4>
        <ul>
          <li v-for="item in queryResults" :key="item.id">
            {{ item.name }} - 蛋白質: {{ item.protein }}g, 熱量: {{ item.calories }}kcal, 脂質: {{ item.fat }}g, 碳水: {{ item.carbo }}g, 餐廳: {{ item.restaurant_name }}
          </li>
        </ul>
      </div>
      <p v-else-if="queried" class="no-results">沒有符合條件的食物</p>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import axios from 'axios';
  
  export default {
    name: 'NutritionQuery',
    setup() {
      const queryResults = ref([]);
      const queried = ref(false);
      const selectedNutrients = ref({ protein: null, calories: null, fat: null, carbo: null });
  
      const nutrients = [
        { key: 'protein', label: '蛋白質' },
        { key: 'calories', label: '熱量' },
        { key: 'fat', label: '脂質' },
        { key: 'carbo', label: '碳水' }
      ];
  
      // 營養素的高低分類
      const selectNutrient = (nutrient, level) => {
        if (selectedNutrients.value[nutrient] === level) {
          selectedNutrients.value[nutrient] = null; // 取消選擇
        } else {
          selectedNutrients.value[nutrient] = level;
        }
      };
  
      // 重置所有選擇
      const resetSelections = () => {
        selectedNutrients.value = { protein: null, calories: null, fat: null, carbo: null };
        queryResults.value = [];
        queried.value = false;
      };
  
      // 查詢食物資料
      const fetchFoods = async () => {
        queried.value = true;
        const hasSelectedNutrients = Object.values(selectedNutrients.value).some(level => level !== null);
        if (!hasSelectedNutrients) {
          alert("請選擇至少一個營養素");
          return;
        }
        try {
          const params = new URLSearchParams();
          for (const [nutrient, level] of Object.entries(selectedNutrients.value)) {
            if (level) {
              params.append('nutrient', nutrient);
              params.append('level', level);
            }
          }
          const response = await axios.get(`http://localhost:5000/foods?${params.toString()}`);
          if (response.data.message) {
            alert(response.data.message);
            queryResults.value = [];
          } else {
            queryResults.value = response.data;
          }
        } catch (error) {
          console.error("查詢失敗:", error);
          alert('查詢失敗，請稍後再試。');
          queryResults.value = [];
        }
      };
  
      return {
        queryResults,
        queried,
        selectedNutrients,
        selectNutrient,
        fetchFoods,
        nutrients,
        resetSelections,
      };
    }
  };
  </script>
  
  <style scoped>
  .nutrition-query-container {
    max-width: 500px;
    margin: 0 auto;
    padding: 50px;
    background-color: #c8fff9;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  .nutrition-title {
    text-align: center;
    font-size: 24px;
    margin-bottom: 30px;
    color: #2e1515;
  }
  
  .nutrition-field {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
  }
  
  .nutrition-field label {
    flex: 1;
    font-size: 18px;
    color: #555;
  }
  
  .nutrition-button {
    padding: 10px 15px;
    border: none;
    border-radius: 4px;
    background-color: #4caf50;
    color: white;
    font-size: 16px;
    cursor: pointer;
    margin-left: 10px;
    transition: background-color 0.3s;
  }
  
  .nutrition-button:hover {
    background-color: #45a049;
  }
  
  .selected {
    background: linear-gradient(to right, #81b5ea, #41c44c);
    color: white;
  }
  
  .query-results {
    margin-top: 20px;
  }
  
  .query-results h4 {
    font-size: 20px;
    margin-bottom: 10px;
    color: #333;
  }
  
  .query-results ul {
    list-style-type: none;
    padding: 0;
  }
  
  .query-results li {
    padding: 8px;
    border-bottom: 1px solid #ddd;
  }
  
  .no-results {
    text-align: center;
    color: #090505;
    font-size: 18px;
    margin-top: 20px;
  }
</style>
  