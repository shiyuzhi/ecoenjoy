import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue'; 
import Delivery from '../views/Delivery.vue';
import Pickup from '../views/Pickup.vue';
import Community from '../views/Community.vue';
import CustomMenu from '../views/CustomMenu.vue';
import Profile from '../views/Profile.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';



const routes = [
  {path: '/', name: 'Home',component: Home,},
  { path: '/delivery', component: Delivery },
  { path: '/pickup', component: Pickup },
  { path: '/community', component: Community },
  { path: '/custom-menu', component: CustomMenu },
  { path: '/profile', name: 'Profile', component: Profile },
  { path: '/Login', component: Login},
  { path: '/Register', component: Register},
  
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
