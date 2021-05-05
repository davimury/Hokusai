import Vue from 'vue'
import Router from 'vue-router'
import Feed from '@/components/Feed'
import Login from '@/components/Login'
import store from '../store';

Vue.use(Router)

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Feed',
      component: Feed,
      meta: {requiresAuth: true},
    },
    {
      path: '/p/:username',
      name: 'Profile',
      component: Feed,
      meta: { guest: true },
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: { guest: true },
    }
  ],
})

router.beforeEach((to, from, next) => {
  console.log(store.getters.isAuthenticated)
  if(to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters.isAuthenticated) {
      next()
      return
    }
    next('/login')
  } else {
    next()
  }
})

export default router
