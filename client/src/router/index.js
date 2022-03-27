import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/invoices',
    name: 'Costs',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import('../views/Costs.vue')
  },
  {
    path: '/invoice/:costId',
    name: 'Cost',
    component: () => import('../views/Cost.vue')
  },
  {
    path: '/new-invoice/:costId',
    name: 'NewCost',
    component: () => import('../views/NewCost.vue')
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: () => import('../views/ForgotPassword.vue')
  },
  {
    path: '/change-password/:key',
    name: 'ChangePassword',
    component: () => import('../views/ChangePassword.vue')
  },
  {
    path: '/my-config',
    name: 'MyConfig',
    component: () => import('../views/MyConfig.vue')
  },
  {
    path: '/products',
    name: 'Products',
    component: () => import('../views/Products.vue')
  },
  {
    path: '/product/:productId',
    name: 'Product',
    component: () => import('../views/Product.vue')
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
