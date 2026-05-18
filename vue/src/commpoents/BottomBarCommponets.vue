<template>
  <footer class="bottombar">
    <div class="bottombar-content">
      <div class="bottombar-links">
        <router-link to="/">首页</router-link>
        <router-link to="/aboutme">关于我</router-link>
      </div>
      <div class="bottombar-copy">&copy; {{ year }} MyBlog. All rights reserved.</div>
    </div>
  </footer>
</template>

<script setup lang="ts">
const year = new Date().getFullYear()
</script>

<style lang="scss" scoped>
.bottombar {
  background-color: #fff;
  box-shadow: 0 -1px 4px rgba(0, 0, 0, 0.08);
  padding: 16px 24px;
  margin-top: auto;
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
    color: #555;
    font-size: 14px;
    transition: color 0.2s;

    &:hover {
      color: #333;
    }
  }
}

.bottombar-copy {
  font-size: 13px;
  color: #999;
}
</style>
