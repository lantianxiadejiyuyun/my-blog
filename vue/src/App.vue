<template>
  <div class="app-layout">
    <TopBarCommponets />
    <main class="app-main">
      <router-view />
    </main>
    <BottomBarCommponets />
  </div>
</template>

<script setup lang="ts">
import TopBarCommponets from "@/component/TopBarCommponets.vue";
import BottomBarCommponets from "@/component/BottomBarCommponets.vue";
</script>

<style lang="scss" scoped>
.app-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: #f7f7f7;
}

.app-main {
  flex: 1;
}
</style>

<style>
.box {
  padding: 20px 0;
  box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.9);
}

.main {

}

*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #f5f5f5;
}

a {
  text-decoration: none;
  color: inherit;
}

ul, ol {
  list-style: none;
}

img {
  max-width: 100%;
  display: block;
}

button, input, textarea {
  font: inherit;
  border: none;
  outline: none;
  background: none;
}

h1, h2, h3, h4, h5, h6 {
  font-weight: 600;
}
</style>
