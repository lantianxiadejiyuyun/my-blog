<template>
  <div class="main">
    <section class="hero">
      <h1>词云</h1>
      <p>用词云发现我的技术关键词</p>
    </section>
    <section class="wordcloud-placeholder">
      <div class="placeholder-card">
        <p>词云组件开发中，敬请期待...</p>
      </div>
    </section>
  </div>
</template>

<style lang="scss" scoped>
.hero {
  text-align: center;
  padding: 4rem 0;

  h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
  }

  p {
    color: #666;
    font-size: 1.1rem;
  }
}

.wordcloud-placeholder {
  display: flex;
  justify-content: center;
  padding: 2rem;

  .placeholder-card {
    width: 100%;
    max-width: 800px;
    min-height: 400px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px dashed #ddd;
    border-radius: 16px;
    background: #fafafa;

    p {
      color: #999;
      font-size: 1.2rem;
    }
  }
}

@media (max-width: 768px) {
  .hero {
    padding: 2rem 0;

    h1 {
      font-size: 1.8rem;
    }
  }

  .wordcloud-placeholder .placeholder-card {
    margin: 0 10px;
    min-height: 300px;
  }
}
</style>
