import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue'; 
import Delivery from '../views/Delivery.vue';
import Profile from '../views/Profile.vue';
import NutritionQuery from '../views/NutritionQuery.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import DietarySuggestions from '../views/DietarySuggestions.vue'; 
import DietLog from '../views/DietLog.vue'; 
import HistoryDiet from '../views/HistoryDiet.vue';
import StoreDetails from '../views/StoreDetails.vue';

const routes = [
  { path: '/', name: 'Home', component: Home }, 
  { path: '/delivery', component: Delivery },
  { path: '/profile', name: 'Profile', component: Profile },
  { path: '/nutrition-query', component: NutritionQuery },
  { path: '/Login', component: Login},
  { path: '/Register', component: Register},
  { path: '/dietary-suggestions', component: DietarySuggestions },
  { path: '/diet-log', component: DietLog }, 
  { path: '/history-diet', name: 'HistoryDiet', component: HistoryDiet},
  { path: '/store/:id', name: 'StoreDetails', component: StoreDetails, props: true,},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
