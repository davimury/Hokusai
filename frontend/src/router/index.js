import Vue from 'vue'
import Router from 'vue-router'
import store from '../store';

Vue.use(Router)

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Feed',
      component: () => import(/*webpackChunkName: "Feed"*/ "../components/Feed.vue"),
      meta: {requiresAuth: true},
    },
    {
      path: '/not-found',
      name: 'NotFoundPage',
      component: () => import(/*webpackChunkName: "NotFoundPage"*/ "../components/NotFoundPage.vue"),
      meta: {requiresAuth: true},
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import(/*webpackChunkName: "Login"*/ "../components/Login.vue"),
      meta: { guest: true },
    },
    {
      path: '/chat',
      name: 'Chat',
      component: () => import(/*webpackChunkName: "Chat"*/ "../components/Chat.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: '/create-post',
      name: 'CreatePost',
      component: () => import(/*webpackChunkName: "CreatePost"*/ "../components/CreatePostPage.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: '/tag/:tag',
      name: 'SearchTag',
      component: () => import(/*webpackChunkName: "SearchConnection"*/ "../components/SearchTag.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: '/:username',
      name: 'Profile',
      component: () => import(/*webpackChunkName: "Profile"*/ "../components/Profile.vue"),
      meta: {requiresAuth: false},
    },
    {
      path: '/statistics',
      name: 'Statistics',
      component: () => import(/*webpackChunkName: "Statistics"*/ "../components/Statistics.vue"),
      meta: {requiresAuth: true},
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
