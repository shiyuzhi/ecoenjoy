<template>
  <div class="diet-log">
    <header>
      <h1>飲食日誌</h1>
      <input type="date" v-model="currentDate" @change="loadDailyLog()" />
      <h2>{{ currentDate }}</h2>
      <div class="calories">
        <h3>營養攝取概覽</h3>
        <div class="nutrient-overview">
          <div class="nutrient-item" v-for="(nutrient, index) in nutrients" :key="index">
            <p>{{ nutrient.label }}: {{ nutrient.current }}g / {{ nutrient.recommended }}g</p>
          </div>
        </div>
      </div>
    </header>
    <div class="food-categories">
      <div v-for="(category, index) in foodCategories" :key="index" class="category">
        <h3>{{ category.label }}</h3>
        <div class="category-info">
          <span>建議：{{ category.recommended }} 份</span>
          <button class="details-button" @click="showDetails(category)">詳細資訊</button>
        </div>
      </div>
    </div>

    <!-- 僅當日期為今天時顯示按鈕 -->
    <button v-if="isToday" class="add-food-button" @click="openAddFoodModal">+ 添加食物</button>

    <h3>已添加食物:</h3>
    <ul>
      <li v-for="food in foods" :key="food.name">
        {{ food.name }} ({{ food.category }}) - 碳水: {{ food.carbs }}g，蛋白質: {{ food.protein }}g，脂肪: {{ food.fat }}g，熱量: {{ food.calories }} kcal
      </li>
    </ul>


    <!-- 添加食物模態框 -->
    <div v-if="showAddFoodModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeAddFoodModal">&times;</span>
        <h3>添加食物</h3>
        <form @submit.prevent="addFood">
          <label for="foodName">食物名稱:</label>
          <input type="text" id="foodName" v-model="newFood.name" required />

          <label for="foodCategory">選擇類別:</label>
          <select v-model="newFood.category" required>
            <option v-for="category in foodCategories" :key="category.label" :value="category.label">
              {{ category.label }}
            </option>
          </select>

          <label for="foodCarbs">碳水化合物 (g):</label>
          <input type="number" id="foodCarbs" v-model.number="newFood.carbs" required />

          <label for="foodProtein">蛋白質 (g):</label>
          <input type="number" id="foodProtein" v-model.number="newFood.protein" required />

          <label for="foodFat">脂肪 (g):</label>
          <input type="number" id="foodFat" v-model.number="newFood.fat" required />

          <label for="foodCalories">熱量 (kcal):</label>
          <input type="number" id="foodCalories" v-model.number="newFood.calories" required />


          <button type="submit">添加</button>
        </form>
      </div>
    </div>

    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <h3>{{ selectedCategory.label }} 詳細資訊</h3>
        <p>攝取建議：{{ selectedCategory.recommended }} 份</p>
        <p>常見食物：{{ selectedCategory.commonFoods.join(', ') }}</p>
        <h4>推薦食物</h4>
        <ul>
          <li v-for="food in selectedCategory.recommendedFoods" :key="food.name">
            {{ food.name }} - {{ food.calories }} 卡路里
            <p>健康益處: {{ food.benefits }}</p>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';

  export default {
  data() {
    const today = new Date();
    const utcDate = new Date(Date.UTC(today.getUTCFullYear(), today.getUTCMonth(), today.getUTCDate()));
    const formattedToday = utcDate.toISOString().slice(0, 10);  // 轉換為 'YYYY-MM-DD'
    console.log("formattedToday (Front-end UTC Date):", formattedToday);  // 除錯輸出
    return {
      currentDate: formattedToday, // 以 YYYY-MM-DD 格式初始化當前日期
      todayDate: formattedToday,
      records: {}, 
      totalCalories: 0, 
      dailyGoal: 2000, 
      nutrients: [
        { label: "碳水化合物", key: "carbs", current: 0, recommended: 300 },
        { label: "蛋白質", key: "protein", current: 0, recommended: 75 },
        { label: "脂肪", key: "fat", current: 0, recommended: 70 },
        { label: "熱量", key: "calories", current: 0, recommended: 2000 }
      ],
      foodLog: {},
      foods: [],
      foodCategories: [
        {
          label: '水果',
          current: 0,
          recommended: 2,
          commonFoods: ['蘋果', '香蕉', '橘子'],
          recommendedFoods: [
            { name: '藍莓', calories: 57, benefits: '富含抗氧化劑，促進心臟健康' },
            { name: '草莓', calories: 32, benefits: '增強免疫系統，富含維生素C' },
            { name: '奇異果', calories: 61, benefits: '促進消化，富含纖維素' }
          ]
        },
        {
          label: '蔬菜',
          current: 0,
          recommended: 3,
          commonFoods: ['胡蘿蔔', '西蘭花', '菠菜'],
          recommendedFoods: [
            { name: '紅椒', calories: 31, benefits: '富含維生素A和C，促進皮膚健康' },
            { name: '南瓜', calories: 26, benefits: '富含纖維，有助於消化' },
            { name: '甘藍', calories: 33, benefits: '富含維生素K，有助於骨骼健康' }
          ]
        },
        {
          label: '全穀類',
          current: 0,
          recommended: 6,
          commonFoods: ['米飯', '全麥麵包', '燕麥'],
          recommendedFoods: [
            { name: '藜麥', calories: 120, benefits: '含有完整蛋白質，促進肌肉增長' },
            { name: '燕麥', calories: 68, benefits: '有助於控制膽固醇水平' },
            { name: '黑米', calories: 160, benefits: '富含抗氧化劑，增強免疫系統' }
          ]
        },
        {
          label: '豆類/蛋白質',
          current: 0,
          recommended: 2,
          commonFoods: ['雞肉', '豆腐', '牛肉'],
          recommendedFoods: [
            { name: '鷹嘴豆', calories: 164, benefits: '富含纖維，促進消化' },
            { name: '鯖魚', calories: 150, benefits: '富含Omega-3脂肪酸，對心臟有益' },
            { name: '蛋', calories: 155, benefits: '高蛋白質，促進肌肉增長' }
          ]
        },
        {
          label: '乳製品',
          current: 0,
          recommended: 2,
          commonFoods: ['牛奶', '酸奶', '起司'],
          recommendedFoods: [
            { name: '低脂牛奶', calories: 42, benefits: '富含鈣質，促進骨骼健康' },
            { name: '酸奶', calories: 59, benefits: '促進腸道健康，富含益生菌' },
            { name: '硬起司', calories: 403, benefits: '富含鈣和蛋白質' }
          ]
        },
        {
          label: '脂肪',
          current: 0,
          recommended: 2,
          commonFoods: ['橄欖油', '堅果', '牛油果'],
          recommendedFoods: [
            { name: '杏仁', calories: 579, benefits: '富含健康脂肪，促進心臟健康' },
            { name: '亞麻籽', calories: 534, benefits: '富含Omega-3脂肪酸，降低炎症' },
            { name: '椰子油', calories: 862, benefits: '促進能量增加，支持新陳代謝' }
          ]
        }
      ],
      showModal: false,
      showAddFoodModal: false,
      selectedCategory: {},
      newFood: {
        name: '',
        category: '',
        carbs: 0,
        protein: 0,
        fat: 0,
        calories: 0
      }
    };
  },
  computed: {
    isToday() {
      return this.currentDate === this.todayDate;
    }
  },
  methods: {
    async loadDailyLog() {
      try {
        const response = await axios.get(`/api/log/${this.currentDate}`);
        const log = response.data;

        this.nutrients.forEach(nutrient => {
          nutrient.current = log[nutrient.key] || 0;
        });

        this.foods = log.foods || [];
      } catch (error) {
        if (error.response && error.response.status === 401) {
          alert("認證失敗，請重新登入！");
          this.$router.push("/login");
        } else {
          console.error("Error loading daily log:", error);
        }
      }
    },
    openAddFoodModal() {
      this.showAddFoodModal = true;
    },
    closeAddFoodModal() {
      this.showAddFoodModal = false;
      this.newFood = { name: '', category: '', carbs: 0, protein: 0, fat: 0, calories: 0 };
    },
    async addFood() {
      const token = localStorage.getItem("token");
      console.log("Token from localStorage: ", token);

      if (!token) {
        alert("請先登入以使用日誌");
        this.$router.push("/login");
        return;
      }

      // 發送新增食物請求
      const response = await axios.post(
        `/api/log`,
        {
          log_date: this.currentDate, // 將日期加入請求主體
          foods: [this.newFood],
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      console.log("API response: ", response)

      // 更新當天的食物清單
      await this.loadDailyLog(); // 確保食物列表更新

      this.closeAddFoodModal();
    },


    showDetails(food) {
      this.selectedCategory = food;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.selectedFood = {};
    }
  },
  mounted() {
    this.loadDailyLog();
  }
};
</script>
  

<style scoped>
/* 整體樣式 */
body {
  font-family: 'Arial', sans-serif;
  background-color: #f4f4f4; /* 淺灰背景 */
  margin: 0;
  padding: 0;
  line-height: 1.6;
}

/* 日誌外框樣式 */
.diet-log {
  padding: 20px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: 30px auto;
}

/* 標題樣式 */
header {
  text-align: center;
  margin-bottom: 20px;
}

h1 {
  font-size: 2.4em;
  color: #34495e;
  font-weight: bold;
}

h2 {
  font-size: 1.6em;
  color: #555555;
}

/* 食物分類區塊 */
.food-categories {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin: 20px 0;
}

.category {
  background-color: #eaeaea;
  border-radius: 10px;
  padding: 15px;
  text-align: center;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.category:hover {
  transform: translateY(-5px);
}

.category h3 {
  color: #3498db;
  font-size: 1.2em;
  margin-bottom: 10px;
}

/* 按鈕樣式 */
.details-button, .add-food-button {
  background-color: #3498db;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  padding: 10px 15px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.3s;
  margin: 10px;
}

.details-button:hover,
.add-food-button:hover {
  background-color: #217dbb;
}

.add-food-button {
  display: block;
  margin: 20px auto;
  font-size: 1.2em;
}

/* 模態框樣式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
  position: relative;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.close {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 18px;
  color: #333333;
  cursor: pointer;
}

.close:hover {
  color: #e74c3c;
}

/* 表單樣式 */
label {
  font-size: 1em;
  color: #555555;
  margin-top: 10px;
  display: block;
}

input[type="text"],
input[type="number"],
select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-bottom: 15px;
}

button {
  background-color: #2ecc71;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #27ae60;
}

/* 營養攝取概覽 */
.nutrient-overview {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.nutrient-item {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 10px;
  text-align: center;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
}

.nutrient-item p {
  font-size: 1em;
  color: #34495e;
}

</style>