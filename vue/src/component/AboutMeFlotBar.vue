<template>
  <div class="floatBar">
    <div class="sidebar-card box">
      <div class="avatar">
        <img src="https://i.pravatar.cc/150" alt="">
        <div class="name">Eugen</div>
        <div class="desc">
          热爱动画与编程的全栈开发工程师，追求简洁高效的代码风格
        </div>
      </div>
    </div>
    <!-- 联系方式 -->
    <div class="sidebar-card box">
      <div class="card-title">联系我</div>
      <div class="list-box">
        <a class="tel-item" href="https://github.com/lantianxiadejiyuyun" target="_blank"
           title="GitHub">
          <img src="/imgs/aboutme/github.svg" alt="GitHub" width="20" height="20">
          <p>Github</p>
        </a>
        <a class="tel-item" href="mailto:2185888430@qq.com" title="Email">
          <img src="/imgs/aboutme/email.svg" alt="Email" width="20" height="20">
          <p>邮箱</p>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">

</script>

<style scoped lang="scss">
.floatBar {

  .sidebar-card {
    padding: 24px;
    margin-bottom: 16px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);

    .avatar {
      display: flex;
      flex-direction: column;
      align-items: center;

      img {
        border-radius: 50%;
        border: 3px solid #fff;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        width: 100px;
        height: 100px;
        object-fit: cover;
      }

      .name {
        margin-top: 12px;
        font-size: 18px;
        font-weight: 600;
        color: #333;
      }

      .desc {
        margin-top: 8px;
        font-size: 13px;
        color: #888;
        text-align: center;
        line-height: 1.6;
      }
    }
  }

  .card-title {
    font-size: 15px;
    font-weight: 600;
    color: #333;
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 2px solid #f0f0f0;
  }

  .list-box {
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;

    .tel-item {
      display: flex;
      align-items: center;
      padding: 0 16px;
      width: 100%;
      height: 42px;
      border-radius: 10px;
      text-decoration: none;
      transition: all 0.25s ease;
      margin-bottom: 10px;

      img {
        margin-right: 10px;
      }

      &:hover {
        background-color: #1677ff;
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(22, 119, 255, 0.35);
        color: #fff;

        img {
          filter: brightness(0) invert(1);
        }
      }
    }
  }
}
</style>
