<template>
  <div class="topbar">
    <div class="topbar-brand">{{ config.blogName }}</div>
    <nav class="topbar-nav">
      <router-link :to="item.path" active-class="active" v-for="(item,i) in routerList" :key="i">
        {{ item.name }}
      </router-link>
    </nav>
    <button class="theme-toggle" @click="toggle" :title="isDark ? '切换浅色' : '切换深色'">
      {{ isDark ? '☀️' : '🌙' }}
    </button>
  </div>
</template>

<script setup lang="ts">
import {config} from '@/config/config'
import {ref} from "vue";
import { useTheme } from '@/composables/useTheme'
const { isDark, toggle } = useTheme()

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
  background-color: var(--bg-card);
  box-shadow: var(--shadow-sm);
  z-index: 999;
  backdrop-filter: blur(10px);
  position: fixed;
  width: 100%;

  .topbar-brand {
    font-size: 20px;
    font-weight: 700;
    color: var(--text-primary);
  }

  .topbar-nav {
    display: flex;
    gap: 24px;
  }

  .topbar-nav a {
    text-decoration: none;
    color: var(--text-secondary);
    font-size: 15px;
    transition: color 0.2s;
  }

  .topbar-nav a:hover {
    color: var(--text-primary);
  }

  .topbar-nav a.active {
    color: var(--color-primary);
    font-weight: 600;
  }

  .theme-toggle {
    cursor: pointer;
    font-size: 18px;
    padding: 6px;
    border-radius: 8px;
    background: transparent;
    transition: background 0.2s;

    &:hover {
      background: var(--border-color);
    }
  }
}

</style>
