import Vue from 'vue';
import VueRouter from 'vue-router';
import Login from '../views/Login.vue';
import ClientMain from '../views/client/Main.vue';
import AdminMain from '../views/admin/Main.vue';
import ClientCredit from '../views/client/Credit.vue';
// import AdminCredit from '../views/admin/Credit.vue';
import ClientRequest from '../views/client/Request.vue';
// import AdminRequest from '../views/admin/Request.vue';
import ClientProfile from '../views/client/Profile.vue';
// import AdminProfile from '../views/admin/Profile.vue';
import ClientLoanApplication from '../views/client/LoanApplication.vue';

Vue.use(VueRouter);

const routes = [
  { path: '/login', component: Login },
  { path: '/client/main', component: ClientMain },
  { path: '/admin/main', component: AdminMain },
  { path: '/client/credit', component: ClientCredit },
  // { path: '/admin/credit', component: AdminCredit },
  { path: '/client/request', component: ClientRequest },
  // { path: '/admin/request', component: AdminRequest },
  { path: '/client/profile', component: ClientProfile },
  // { path: '/admin/profile', component: AdminProfile },
  { path: '/client/loan-application', component: ClientLoanApplication },

];

const router = new VueRouter({
  routes,
});

export default router;
