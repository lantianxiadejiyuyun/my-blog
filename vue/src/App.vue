<template>
  <div class="app-layout">
    <TopBarCommponets />
    <main class="app-main">
      <router-view />
    </main>
    <footer class="app-footer">
      <BottomBarCommponets />
    </footer>
  </div>
</template>

<script setup lang="ts">
import TopBarCommponets from "@/commpoents/TopBarCommponets.vue";
import BottomBarCommponets from "@/commpoents/BottomBarCommponets.vue";
</script>

<style lang="scss" scoped>
.app-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-main {
  flex: 1;
}
</style>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
</style>
