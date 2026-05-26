<template>
  <div class="topbar">
    <div class="topbar-brand">{{ config.blogName }}</div>
    <nav class="topbar-nav">
      <router-link :to="item.path" active-class="active" v-for="(item,i) in routerList" :key="i">
        {{ item.name }}
      </router-link>
    </nav>
  </div>
</template>

<script setup lang="ts">
import {config} from '@/config/config'
import {ref} from "vue";

const routerList = ref([
  {
    path: "/",
    name: "首页",
    icon: ''
  }, {
    path: "/wordcloud",
    name: "词云",
    icon: ''
  }, {
    path: "/aboutme",
    name: "关于",
    icon: ''
  }, {
    path: "/aboutme",
    name: "关于",
    icon: ''
  }, {
    path: "/aboutme",
    name: "关于",
    icon: ''
  }
])
</script>

<style scoped>
.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 80px;
  background-color: rgb(255 255 255 / 0.6);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  z-index: 999;
  backdrop-filter: blur(10px);
  position: fixed;
  width: 100%;

  .topbar-brand {
    font-size: 20px;
    font-weight: 700;
    color: #333;
  }

  .topbar-nav {
    display: flex;
    gap: 24px;
  }

  .topbar-nav a {
    text-decoration: none;
    color: #555;
    font-size: 15px;
    transition: color 0.2s;
  }

  .topbar-nav a:hover {
    color: #333;
  }

  .topbar-nav a.active {
    color: #1677ff;
    font-weight: 600;
  }
}

</style>
