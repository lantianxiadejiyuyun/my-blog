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

@media (max-width: 768px) {
  .hero {
    padding: 2rem 0;

    h1 {
      font-size: 1.8rem;
    }
  }

  .wordcloud-placeholder {
    .placeholder-card {
      margin: 0 10px;
      min-height: 300px;
    }
  }
}
.hero {
  margin-top: 4rem;
  text-align: center;
  padding: 4rem 0;

  h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
  }

  p {
    color: var(--text-secondary);
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
    border: 2px dashed var(--border-light);
    border-radius: 16px;
    background: var(--bg-tertiary);

    p {
      color: var(--text-muted);
      font-size: 1.2rem;
    }
  }
}


</style>
