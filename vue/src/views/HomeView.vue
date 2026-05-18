<template>
  <div class="main">
    <section class="hero">
      <h1>欢迎来到我的博客</h1>
      <p>记录技术成长，分享编程心得</p>
    </section>

    <section class="content">
      <article class="post" v-for="n in 3" :key="n">
        <h2>文章标题 {{ n }}</h2>
        <p class="meta">2026-05-14 · 阅读约 5 分钟</p>
        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor
          incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud
          exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
        </p>
      </article>
    </section>
  </div>
</template>

<style lang="scss" scoped>
.main {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.hero {
  text-align: center;
  padding: 4rem 0;
}

.hero h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.hero p {
  color: #666;
  font-size: 1.1rem;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.post {
  padding: 1.5rem;
  border: 1px solid #eee;
  border-radius: 8px;
}

.post h2 {
  margin-bottom: 0.3rem;
}

.meta {
  color: #999;
  font-size: 0.85rem;
  margin-bottom: 1rem;
}
</style>
