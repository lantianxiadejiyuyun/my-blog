import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path:'/', name:'home',component:() => import ('@/views/HomeView.vue')
    },
    {
      path:'/aboutme', name:'about',component:() => import('@/views/AboutMe.vue')
    },
    {
      path:'/wordcloud', name:'wordcloud',component:() => import('@/views/WordCloud.vue')
    }
  ],
})

router.afterEach(() => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
})

export default router
