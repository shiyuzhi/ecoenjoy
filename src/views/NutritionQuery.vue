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
    max-width: 600px;
    margin: 0 auto;
    padding: 50px;
    background: linear-gradient(135deg, #00bcd4, #6ae46e); 
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
    animation: fadeIn 1s ease-out;
  }
  
  @keyframes fadeIn {
    0% {
      opacity: 0;
    }
    100% {
      opacity: 1;
    }
  }
  
  .nutrition-title {
    text-align: center;
    font-size: 28px;
    margin-bottom: 30px;
    color: #f5f0f0;
    font-weight: 700;
  }
  
  .nutrition-field {
    display: flex;
    align-items: center; 
    margin-bottom: 18px;
    gap: 20px; 
    margin-left: 40px;
  }
  
  .nutrition-field label {
    flex: 1; 
    font-size: 18px;
    color: #000000;
    font-weight: 500;
    margin: 0; 
    text-align: left;
  }

  .nutrition-button {
    padding: 12px 18px;
    border: none;
    border-radius: 8px;
    background-color: #080402; 
    color: white;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.2s, box-shadow 0.2s;
    box-shadow: 0 5px 15px rgba(255, 87, 34, 0.4);
  }
  
  .nutrition-button:hover {
    background-color: #e64a19; 
    transform: translateY(-3px);
    box-shadow: 0 5px 20px rgba(255, 87, 34, 0.6);
  }
  
  .selected {
    background: linear-gradient(to right, #020501e3, #100202e3);
    color: white;
    font-weight: 600;
  }
  
  .query-results {
    margin-top: 15px;
  }
  
  .query-results h4 {
    font-size: 22px;
    margin-bottom: 15px;
    color: #ffffff;
  }
  
  .query-results ul {
    list-style-type: none;
    padding: 0;
  }
  
  .query-results li {
    padding: 20px;
    background-color: #ffffff;
    margin-bottom: 8px;
    border-radius: 8px;
    border: 1px solid #e0e0e0;
    transition: background-color 0.3s ease, box-shadow 0.2s;
  }
  
  .query-results li:hover {
    background-color: #b2dfdb;
    border-color: #00bcd4;
    box-shadow: 0 4px 12px rgba(0, 188, 212, 0.3);
  }
  
  .no-results {
    text-align: center;
    color: #000000;
    font-size: 18px;
    margin-top: 25px;
    font-weight: 500;
  }
</style>
