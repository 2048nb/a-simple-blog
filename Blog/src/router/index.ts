import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/home',
    },
    {
      path: '/home',
      component: () => import('@/views/home.vue'),
    },
    {
      path: '/publish',
      component: () => import('@/views/publish.vue'),
    },
    {
      path: '/login',
      component: () => import('@/views/login.vue'),
    },
    {
      path: '/register',
      component: () => import('@/views/register.vue'),
    },
    {
      path: '/mycollection',
      component: () => import('@/views/myCollection.vue'),
    },
    {
      path: '/myposts',
      component: () => import('@/views/myPosts.vue'),
    },
    {
      path: '/postdetail/:post_id',
      name: 'postDetail',
      component: () => import('@/views/postDetail.vue'),
    }
  ],
})

export default router
