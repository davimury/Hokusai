import Vue from 'vue'
import Router from 'vue-router'
import Feed from '@/components/Feed'
import Login from '@/components/Login'
import Profile from '@/components/Profile'
import SavedPosts from '@/components/SavedPosts'
import CreatePost from '@/components/CreatePost'
import Chat from '@/components/Chat'
import SearchConnection from '@/components/SearchConnection'
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
      path: '/login',
      name: 'Login',
      component: Login,
      meta: { guest: true },
    },
    {
      path: '/saved',
      name: 'SavedPosts',
      component: SavedPosts,
      meta: { requiresAuth: true },
    },
    {
      path: '/chat',
      name: 'Chat',
      component: Chat,
      meta: { requiresAuth: true },
    },
    {
      path: '/create-post',
      name: 'CreatePost',
      component: CreatePost,
      meta: { requiresAuth: true },
    },
    {
      path: '/search',
      name: 'SearchConnection',
      component: SearchConnection,
      meta: { requiresAuth: true },
    },
    {
      path: '/:username',
      name: 'Profile',
      component: Profile,
      meta: {requiresAuth: false},
    },
  ],
})
router.beforeResolve((to, from, next) => {
  // If this isn't an initial page load.
  if (to.name) {
    // Start the route progress bar.
    console.log(1)
  }
  next()
})

router.afterEach((to, from) => {
  // Complete the animation of the route progress bar.
  console.log(2)
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
