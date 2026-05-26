<template>
  <div class="content" @click="gotoTop()">Top</div>
</template>

<script setup lang="ts">

const gotoTop = () => {
  window.scrollTo({top: 0, behavior: 'smooth'});
}

</script>


<style scoped lang="scss">
.content {
  position: fixed;
  bottom: 120px;
  right: 60px;
  border-radius: 50%;
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  padding: 20px;
  cursor: pointer;
  transition: 0.3s;
  z-index: 999;

  &:hover {
    background: var(--color-primary);
    color: #fff;
  }
}
</style>
