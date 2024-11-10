import { createRouter, createWebHistory } from 'vue-router';
import Main from '../views/Main.vue';
import Credit from '../views/Credit.vue';
import Request from '../views/Request.vue';
import Profile from '../views/Profile.vue';
import LoanApplication from '../views/LoanApplication.vue';
import Login from '../views/Login.vue';

const routes = [
  { path: '/', component: Main },
  { path: '/credit', component: Credit },
  { path: '/request', component: Request },
  { path: '/profile', component: Profile },
  { path: '/loan-application', component: LoanApplication },
  { path: '/login', component: Login, meta: { hideNavBar: true } } 
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;