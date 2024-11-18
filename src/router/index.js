import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue'; 
import Delivery from '../views/Delivery.vue';
import Pickup from '../views/Pickup.vue';
import Community from '../views/Community.vue';
import CustomMenu from '../views/CustomMenu.vue';
import Profile from '../views/Profile.vue';
import NutritionQuery from '../views/NutritionQuery.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import DietarySuggestions from '../views/DietarySuggestions.vue'; 
import DietLog from '../views/DietLog.vue'; 
import HistoryDiet from '../views/HistoryDiet.vue';

const routes = [
  {path: '/', name: 'Home',component: Home,},
  { path: '/delivery', component: Delivery },
  { path: '/pickup', component: Pickup },
  { path: '/community', component: Community },
  { path: '/custom-menu', component: CustomMenu },
  { path: '/profile', name: 'Profile', component: Profile },
  { path: '/nutrition-query', component: NutritionQuery },
  { path: '/Login', component: Login},
  { path: '/Register', component: Register},
  { path: '/dietary-suggestions', component: DietarySuggestions },
  { path: '/diet-log', component: DietLog }, 
  { path: '/history-diet', name: 'HistoryDiet', component: HistoryDiet,

  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
