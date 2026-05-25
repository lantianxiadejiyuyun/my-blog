<template>
  <div class="server-info box">
    <div class="title">服务器信息</div>
    <div class="placeholder">暂无数据</div>
  </div>
</template>

<script setup lang="ts">

</script>

<style scoped lang="scss">
.server-info {
  padding: 24px;

  .title {
    font-size: 16px;
    font-weight: 600;
    color: #333;
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 2px solid #f0f0f0;
  }

  .placeholder {
    text-align: center;
    color: #bbb;
    font-size: 13px;
    padding: 40px 0;
  }
}
</style>
