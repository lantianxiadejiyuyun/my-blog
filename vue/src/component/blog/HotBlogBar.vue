<template>
  <div class="hot-blog box">
    <div class="title">热门文章</div>
    <div class="list">
      <div class="item" v-for="(item, i) in hotBlogList" :key="i">
        <span class="rank" :class="{ top: i < 3 }">{{ i + 1 }}</span>
        <span class="name">{{ item.title }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  hotBlogList: { title: string ,id: number }[];
}>()
</script>

<style scoped lang="scss">


.hot-blog {
  padding: 24px;

  .title {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 2px solid var(--border-color);
  }

  .list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .item {
    display: flex;
    align-items: center;
    cursor: pointer;

    &:hover .name {
      color: var(--color-primary);
    }

    .rank {
      flex-shrink: 0;
      width: 22px;
      height: 22px;
      border-radius: 6px;
      background: var(--border-color);
      color: var(--text-muted);
      font-size: 12px;
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: 10px;

      &.top {
        background: var(--color-primary);
        color: #fff;
      }
    }

    .name {
      font-size: 13px;
      color: var(--text-secondary);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      transition: color 0.2s;
    }
  }
}
</style>
