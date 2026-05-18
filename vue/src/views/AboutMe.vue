
<template>
  <div class="content">
    <!-- 留一个空间 -->
    <div class="header-box">

    </div>
    <div class="main">
      <!--个人介绍-->
      <div class="introduction-box">
        <div class="avatar">
          <img src="https://i.pravatar.cc/150" alt="">
        </div>
        <!-- 联系方式 比如github qq wechat 什么的 -->
        <div class="tel-box">
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
      <!--履历-->
      <div class="resume-box">

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {onMounted, onUnmounted} from 'vue'

onMounted(()=>{

})

onUnmounted(()=>{

})
</script>

<style lang="scss" scoped>
.content {


  .main {
    max-width: 1600px;
    min-width: 1000px;
    min-height: 100vh;
    margin: 0 auto;

    display: flex;
    justify-content: space-between;

    .introduction-box {
      flex:3;
      padding: 10px;

      background-color: #16ffc1;
      height: 2000px;
      border: 1px solid gainsboro;

      .tel-box {
        display: flex;
        justify-content: center;
        gap: 12px;
        margin-top: 16px;
        padding: 12px 0;
        border-top: 1px solid rgba(0, 0, 0, 0.06);
      }

      .tel-item {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: rgba(0, 0, 0, 0.06);
        text-decoration: none;
        transition: all 0.2s;

        &:hover {
          background-color: #1677ff;

          img {
            filter: brightness(0) invert(1);
          }
        }
      }
    }

    .resume-box {
      margin: 0 0 0 10px;
      padding: 10px;
      border: 1px solid gainsboro;
      flex:7;
      background-color: #1677ff;
      height: 2000px;
    }
  }
}
</style>
