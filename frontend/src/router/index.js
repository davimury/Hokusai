import Vue from 'vue'
import Router from 'vue-router'
import Feed from '@/components/Feed'
import Login from '@/components/Login'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Feed',
      component: Feed
    },
    {
      path: '/p/:username',
      name: 'Profile',
      component: Feed
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    }
  ]
})
