<template>
  <article class="container box">
    <div class="img">
      <img :src="imgPath" alt="">
    </div>
    <div class="description">
      <div class="title">{{ title }}</div>
      <div class="categories">
        <i class="fi fi-ss-flag"></i> <span class="tag" v-for="(item,i) in categories" :key="i">{{ item.name }}</span>
      </div>
      <div class="meta">{{ meta }}</div>
      <div class="description">{{ description }}</div>
    </div>
  </article>
</template>

<script setup lang="ts">
import {BlogCategories} from '@/type/blogCategory'

defineProps<{
  title: string,
  description: string,
  imgPath?: string,
  meta: string,
  categories: BlogCategories [],
}>()

</script>

<style scoped lang="scss">
.container {
  display: flex;
  padding: 20px;
  cursor: pointer;
  transition: transform 0.25s ease, box-shadow 0.25s ease;

  &:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
  }

  .img {
    flex-shrink: 0;
    width: 220px;
    height: 140px;
    overflow: hidden;
    border-radius: 8px;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }

  .description {
    flex: 1;
    padding: 0 0 0 20px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-width: 0;
    overflow: hidden;

    .title {
      font-size: 17px;
      font-weight: 600;
      color: var(--text-title);
      margin-bottom: 6px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .meta {
      font-size: 12px;
      color: var(--text-muted);
      margin-bottom: 8px;
    }

    .categories {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      margin-bottom: 8px;

      .tag {
        font-size: 11px;
        padding: 2px 10px;
        border-radius: 20px;
        background: var(--color-primary-bg);
        color: var(--color-primary);
        transition: background 0.2s, color 0.2s;
        cursor: pointer;

        &:hover {
          background: var(--color-primary);
          color: #fff;
        }
      }
    }

    .description {
      font-size: 13px;
      color: var(--text-secondary);
      line-height: 1.6;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
  }
}

@media (max-width: 768px) {
  .container {
    .img {
      width: 100px;
      height: 80px;
    }

    .description {
      padding: 0 0 0 12px;

      .title {
        font-size: 15px;
      }
    }
  }
}
</style>
