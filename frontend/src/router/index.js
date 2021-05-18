import Vue from 'vue'
import Router from 'vue-router'
import Feed from '@/components/Feed'
import Login from '@/components/Login'
import Profile from '@/components/Profile'
import SavedPosts from '@/components/SavedPosts'
import CreatePost from '@/components/CreatePost'
import Chat from '@/components/Chat'
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
      path: '/profile',
      name: 'Profile',
      component: Profile,
      meta: { guest: true },
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: { guest: true },
    },
    {
      path: '/saved',
      name: 'SavedPosts',
      component: SavedPosts,
      meta: { guest: true },
    },
    {
      path: '/chat',
      name: 'Chat',
      component: Chat,
      meta: { guest: true },
    },
    {
      path: '/create-post',
      name: 'CreatePost',
      component: CreatePost,
      meta: { guest: true },
    },
  ],
})

router.beforeEach((to, from, next) => {
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
