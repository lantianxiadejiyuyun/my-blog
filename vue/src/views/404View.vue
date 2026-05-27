<template>
  <div class="not-found">
    <h1 class="not-found__code">404</h1>
    <p class="not-found__text">页面不存在</p>
    <router-link to="/" class="not-found__btn">返回首页</router-link>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter();

onMounted(() => {
  setTimeout(() => {
    router.push('/');
  },3000)
})
</script>

<style scoped lang="scss">
.not-found {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 80px - 60px); // 减去TopBar和BottomBar的高度
  color: var(--text-secondary);

  &__code {
    font-size: 96px;
    font-weight: 800;
    color: var(--color-primary);
    line-height: 1;
  }

  &__text {
    font-size: 18px;
    margin: 16px 0 32px;
  }

  &__btn {
    padding: 10px 32px;
    border-radius: 8px;
    background: var(--color-primary);
    color: #fff;
    font-size: 15px;
    transition: opacity 0.2s;

    &:hover {
      opacity: 0.85;
    }
  }
}
</style>
