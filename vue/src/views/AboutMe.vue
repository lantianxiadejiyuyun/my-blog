<template>
  <div class="content">
    <!-- 留一个空间 -->
    <div class="header-box">

    </div>
    <div class="main">
      <!--个人介绍-->
      <div class="introduction-box">
        <div class="sidebar-card">
          <div class="avatar">
            <img src="https://i.pravatar.cc/150" alt="">
            <div class="name">Eugen</div>
          </div>
        </div>
        <!-- 联系方式 -->
        <div class="sidebar-card">
          <div class="card-title">联系我</div>
          <div class="list-box">
            <a class="tel-item" href="https://github.com" target="_blank" title="GitHub">
              <img src="../../imgs/aboutme/github.svg" alt="GitHub" width="20" height="20">
            </a>
            <a class="tel-item" href="mailto:your@email.com" title="Email">
              <img src="../../imgs/aboutme/email.svg" alt="Email" width="20" height="20">
            </a>
            <a class="tel-item" href="#" title="QQ">
              <img src="../../imgs/aboutme/qq.svg" alt="QQ" width="20" height="20">
            </a>
            <a class="tel-item" href="https://gitee.com" target="_blank" title="Gitee">
              <img src="../../imgs/aboutme/gitee.svg" alt="Gitee" width="20" height="20">
            </a>
          </div>
        </div>
      </div>
      <!--履历-->
      <div class="resume-box">

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {onMounted, onUnmounted} from 'vue'

onMounted(() => {

})

onUnmounted(() => {

})
</script>

<style lang="scss" scoped>
.content {
  .header-box {
    width: 100%;
    background: linear-gradient(to bottom, rgba(0, 0, 0, 0), rgba(255, 255, 255, 0.9)), url("../../public/imgs/aboutme/top-back.png");
    background-repeat: no-repeat;
    background-size: cover;
    height: 40vh;
  }

  .box {
    padding: 20px 0;
    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
    margin-bottom:20px;
  }

  .main {
    max-width: 1600px;
    min-width: 1000px;
    min-height: 100vh;
    margin: 0 auto;

    display: flex;
    justify-content: space-between;

    .introduction-box {
      flex: 3;

      .sidebar-card {
        background: #fff;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
      }

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
        justify-content: space-evenly;

        .tel-item {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 42px;
          height: 42px;
          border-radius: 50%;
          background-color: #f5f5f5;
          text-decoration: none;
          transition: all 0.25s ease;

          &:hover {
            background-color: #1677ff;
            transform: translateY(-3px);
            box-shadow: 0 4px 12px rgba(22, 119, 255, 0.35);

            img {
              filter: brightness(0) invert(1);
            }
          }
        }
      }
    }

    .resume-box {
      margin: 0 0 0 10px;
      padding: 10px;
      border: 1px solid gainsboro;
      flex: 7;
      background-color: #1677ff;
      height: 2000px;
    }
  }
}
</style>
