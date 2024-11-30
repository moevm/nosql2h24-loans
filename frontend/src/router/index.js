import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import ClientMain from '../views/client/Main.vue';
import AdminMain from '../views/admin/Main.vue';
import ClientCredit from '../views/client/Credit.vue';
import ClientRequest from '../views/client/Request.vue';
import AdminRequest from '../views/admin/Request.vue';
import ClientProfile from '../views/client/Profile.vue';
import AdminProfile from '../views/admin/Profile.vue';
import ClientLoanApplication from '../views/client/LoanApplication.vue';

const routes = [
  // { path: '/', redirect: '/login' },
  { path: '/login', component: Login, meta: { hideNavBar: true } },
  { path: '/register', component: Register, meta: { hideNavBar: true } },
  { path: '/client/main', component: ClientMain },
  { path: '/admin/main', component: AdminMain },
  { path: '/client/credit', component: ClientCredit },
  { path: '/client/request', component: ClientRequest },
  { path: '/admin/request', component: AdminRequest },
  { path: '/client/profile', component: ClientProfile },
  { path: '/admin/profile', component: AdminProfile },
  { path: '/client/loan-application', component: ClientLoanApplication },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
