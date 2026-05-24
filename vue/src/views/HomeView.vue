<template>
  <div class="main">
    <section class="hero">
      <h1>欢迎来到我的博客</h1>
      <p>记录技术成长，分享编程心得</p>
    </section>

    <section class="content">
      <BlogProfileBar :title="item.title + i+1" :meta="item.meta" :categories="item.categories" :description="item.description"
                      :imgPath="item.imgPath"
                      v-for="(item,i) in blogList" :key="i"></BlogProfileBar>
    </section>
  </div>
</template>

<script setup lang="ts">
import BlogProfileBar from "@/component/blog/BlogProfileBar.vue";

import {ref} from "vue";

const blogList = ref([
  {
    title: 'Vue3 组合式 API 实战总结',
    meta: '2026-05-20 · 阅读约 8 分钟',
    imgPath: '/imgs/home/index.jpg',
    description: '从选项式到组合式的迁移经验，分享 setup 语法糖和 composables 的最佳实践',
    categories: [{ id: '1', name: 'Vue' }, { id: '2', name: '前端' }]
  },
  {
    title: 'TypeScript 泛型入门指南',
    meta: '2026-05-18 · 阅读约 6 分钟',
    imgPath: '/imgs/home/index.jpg',
    description: '用实际案例讲透泛型的用法，从基础约束到条件类型的进阶技巧',
    categories: [{ id: '3', name: 'TypeScript' }, { id: '2', name: '前端' }]
  },
  {
    title: 'CSS Grid 布局完全攻略',
    meta: '2026-05-15 · 阅读约 5 分钟',
    imgPath: '/imgs/home/index.jpg',
    description: '一篇文章掌握 Grid 所有核心属性，附带常见布局模板',
    categories: [{ id: '4', name: 'CSS' }, { id: '2', name: '前端' }]
  },
  {
    title: 'Node.js 后端接口开发踩坑记录',
    meta: '2026-05-12 · 阅读约 7 分钟',
    imgPath: '/imgs/home/index.jpg',
    description: '记录 Express + MongoDB 开发中遇到的坑及解决方案',
    categories: [{ id: '5', name: 'Node.js' }, { id: '6', name: '后端' }]
  },
  {
    title: 'Uniapp 跨端开发经验分享',
    meta: '2026-05-10 · 阅读约 6 分钟',
    imgPath: '/imgs/home/index.jpg',
    description: '从 Web 到小程序再到 App，一套代码多端运行的真实体验',
    categories: [{ id: '7', name: 'Uniapp' }, { id: '2', name: '前端' }]
  },
  {
    title: '前端性能优化清单',
    meta: '2026-05-08 · 阅读约 9 分钟',
    imgPath: '/imgs/home/index.jpg',
    description: '从加载到渲染，梳理前端性能优化的关键节点和实操方法',
    categories: [{ id: '2', name: '前端' }, { id: '8', name: '性能优化' }]
  },
  {
    title: 'Python 爬虫入门到实战',
    meta: '2026-05-05 · 阅读约 7 分钟',
    imgPath: '/imgs/home/index.jpg',
    description: '用 requests + BeautifulSoup 快速上手爬虫，附反爬应对策略',
    categories: [{ id: '9', name: 'Python' }, { id: '6', name: '后端' }]
  },
  {
    title: 'Git 团队协作流程规范',
    meta: '2026-05-02 · 阅读约 4 分钟',
    imgPath: '/imgs/home/index.jpg',
    description: '分支管理、提交规范、Code Review 流程，团队开发必看',
    categories: [{ id: '10', name: 'Git' }, { id: '11', name: '工程化' }]
  },
  {
    title: 'Pinia 状态管理最佳实践',
    meta: '2026-04-28 · 阅读约 5 分钟',
    imgPath: '/imgs/home/index.jpg',
    description: '为什么选 Pinia 而不是 Vuex，以及在项目中如何优雅地组织 Store',
    categories: [{ id: '1', name: 'Vue' }, { id: '2', name: '前端' }]
  },
  {
    title: '从零搭建个人博客全记录',
    meta: '2026-04-25 · 阅读约 10 分钟',
    imgPath: '/imgs/home/index.jpg',
    description: '这个博客从规划到上线的完整过程，技术选型与踩坑全分享',
    categories: [{ id: '12', name: '项目实战' }, { id: '2', name: '前端' }]
  },
])

</script>

<style lang="scss" scoped>

.hero {
  text-align: center;
  padding: 4rem 0;

  .hero h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
  }

  .hero p {
    color: #666;
    font-size: 1.1rem;
  }
}
</style>
