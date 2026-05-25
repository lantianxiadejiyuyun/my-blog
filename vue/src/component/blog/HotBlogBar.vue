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
    color: #333;
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 2px solid #f0f0f0;
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
      color: #1677ff;
    }

    .rank {
      flex-shrink: 0;
      width: 22px;
      height: 22px;
      border-radius: 6px;
      background: #f0f0f0;
      color: #999;
      font-size: 12px;
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: 10px;

      &.top {
        background: #1677ff;
        color: #fff;
      }
    }

    .name {
      font-size: 13px;
      color: #555;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      transition: color 0.2s;
    }
  }
}
</style>
