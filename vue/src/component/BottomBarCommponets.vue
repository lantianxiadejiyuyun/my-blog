<template>
  <footer class="bottombar">
    <div class="bottombar-content">
      <div class="bottombar-links">
        <router-link to="/">首页</router-link>
        <router-link to="/aboutme">关于我</router-link>
      </div>
      <div class="bottombar-friends">
        <span class="friends-label">友情链接</span>
        <a v-for="item in friendLinks" :key="item.name" :href="item.url" target="_blank">
          <img :src="item.icon" :alt="item.name">
          {{ item.name }}
        </a>
      </div>
      <div class="bottombar-copy">&copy; {{ year }} MyBlog. All rights reserved.</div>
    </div>
  </footer>
</template>

<script setup lang="ts">
const year = new Date().getFullYear()

const friendLinks = [
  { name: 'GitHub', url: 'https://github.com', icon: '/imgs/aboutme/github.svg' },
  { name: 'Gitee', url: 'https://gitee.com', icon: '/imgs/aboutme/github.svg' },
]
</script>

<style lang="scss" scoped>
.bottombar {
  background-color: var(--bg-card);
  box-shadow: var(--shadow-sm);
  padding: 16px 24px;
  margin-top: auto;
  z-index: 9;
}

.bottombar-content {
  max-width: 960px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.bottombar-links {
  display: flex;
  gap: 16px;

  a {
    text-decoration: none;
    color: var(--text-secondary);
    font-size: 14px;
    transition: color 0.2s;

    &:hover {
      color: var(--text-primary);
    }
  }
}

.bottombar-copy {
  font-size: 13px;
  color: var(--text-muted);
}

.bottombar-friends {
  display: flex;
  align-items: center;
  gap: 16px;

  .friends-label {
    font-size: 13px;
    color: var(--text-muted);
  }

  a {
    display: flex;
    align-items: center;
    gap: 4px;
    text-decoration: none;
    color: var(--text-secondary);
    font-size: 13px;
    transition: color 0.2s;

    img {
      width: 16px;
      height: 16px;
    }

    &:hover {
      color: var(--color-primary);
    }
  }
}

@media (max-width: 768px) {
  .bottombar-content {
    flex-direction: column;
    gap: 12px;
    text-align: center;
  }
}
</style>
