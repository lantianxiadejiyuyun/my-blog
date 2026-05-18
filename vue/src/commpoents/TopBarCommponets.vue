<template>
  <div class="topbar">
    <div class="topbar-brand">MyBlog</div>
    <nav class="topbar-nav">
      <router-link to="/" exact-active-class="active">首页</router-link>
      <router-link to="/aboutme" active-class="active">关于我</router-link>
    </nav>
  </div>
</template>

<script setup lang="ts">

</script>

<style scoped>
.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 56px;
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
}

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
</style>
