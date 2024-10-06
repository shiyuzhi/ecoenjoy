<template>
  <div class="custom-menu">
    <h2>自定義菜單</h2>
    
    <div class="staples">
      <h3>選擇主食</h3>
      <label v-for="staple in staples" :key="staple.id" class="staple-label">
        <input type="radio" v-model="selectedStaple" :value="staple.name" />
        {{ staple.name }}
      </label>
    </div>
    
    <div class="ingredients">
      <h3>選擇配料</h3>
      <label v-for="ingredient in ingredients" :key="ingredient.id" class="ingredient-label">
        <input type="checkbox" v-model="selectedIngredients" :value="ingredient.name" />
        {{ ingredient.name }}
      </label>
    </div>

    <div class="customized-menu">
      <h3>您的自定義菜單</h3>
      <p v-if="!selectedStaple && selectedIngredients.length === 0">尚未選擇任何主食或配料</p>
      <p v-if="selectedStaple">主食: {{ selectedStaple }}</p>
      <ul>
        <li v-for="ingredient in selectedIngredients" :key="ingredient">{{ ingredient }}</li>
      </ul>
    </div>

    <button @click="saveCustomMenu" class="save-button">保存自定義菜單</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      staples: [
        { id: 1, name: '白飯' },
        { id: 2, name: '麵食' },
      ],
      ingredients: [
        { id: 1, name: '雞肉' },
        { id: 2, name: '牛肉' },
        { id: 3, name: '蔬菜' },
        { id: 4, name: '海鮮' },
      ],
      selectedStaple: '',
      selectedIngredients: [],
    };
  },
  methods: {
    saveCustomMenu() {
      if (this.selectedStaple || this.selectedIngredients.length > 0) {
        alert('自定義菜單已保存！');
        console.log('選擇的主食:', this.selectedStaple);
        console.log('選擇的配料:', this.selectedIngredients);
      } else {
        alert('請選擇主食或配料以保存自定義菜單');
      }
    },
  },
};
</script>

<style scoped>
.custom-menu {
  padding: 20px;
  border: 2px solid #343a40; 
  background: linear-gradient(to right, #ffffff); 
  border-radius: 15px; 
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3); 
  color: #333; 
}

.staples, .ingredients {
  margin-bottom: 10px;
}

.staple-label, .ingredient-label {
  display: block; 
  padding: 20px; 
  border: 1px solid #2b2424; 
  border-radius: 5px; 
  margin-bottom: 10px; 
  background-color: #ffffff; 
  transition: background-color 0.3s; 
}

.staple-label:hover, .ingredient-label:hover {
  background-color: #c8eed1;
}

.customized-menu {
  margin-bottom: 20px;
  padding: 10px; 
  background: #ffffff; 
  border: 1px solid #ddd; 
  border-radius: 20px; 
}

.save-button {
  background-color: #2f2a29;
  color: white; 
  border: none; 
  border-radius: 5px; 
  padding: 10px 15px; 
  cursor: pointer; 
  transition: background-color 0.3s; 
}

.save-button:hover {
  background-color: #9d7a70; 
}
</style>
