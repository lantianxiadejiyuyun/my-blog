<template>
  <div class="content">
    <!-- 留一个空间 -->
    <div class="header-box">

    </div>
    <div class="main">
      <!--个人介绍-->
      <div class="introduction-box">
        <div class="sidebar-card box">
          <div class="avatar">
            <img src="https://i.pravatar.cc/150" alt="">
            <div class="name">Eugen</div>
          </div>
        </div>
        <!-- 联系方式 -->
        <div class="sidebar-card box">
          <div class="card-title">联系我</div>
          <div class="list-box">
            <a class="tel-item" href="https://github.com/lantianxiadejiyuyun" target="_blank"
               title="GitHub">
              <img src="../../imgs/aboutme/github.svg" alt="GitHub" width="20" height="20">
              <p>Github</p>
            </a>
            <a class="tel-item" href="mailto:your@email.com" title="Email">
              <img src="../../imgs/aboutme/email.svg" alt="Email" width="20" height="20">
              <p>邮箱</p>
            </a>
          </div>
        </div>
      </div>
      <!--履历-->
      <div class="resume-box">
        <div class="skill-treee box">
          <div class="title">
            我的技能树
          </div>
          <div class="tree-message">
            <div class="tree-item">
              <img src="../../public/imgs/aboutme/skill-tree/web.png" alt="前端开发">
              <p>前端开发</p>
            </div>
            <div class="skill-list">
              <div
                v-for="(skill, index) in myScoreConfig.web"
                :key="index"
                class="skill-item"
              >
                <div class="skill-ring">
                  <svg viewBox="0 0 120 120">
                    <circle class="ring-bg" cx="60" cy="60" r="52" />
                    <circle
                      class="ring-progress"
                      cx="60" cy="60" r="52"
                      :style="{
                        strokeDashoffset: 327 * (1 - skill.score / 100),
                        stroke: skill.backcolor || '#1677ff'
                      }"
                    />
                  </svg>
                  <span class="ring-name">{{ skill.name }}</span>
                </div>
              </div>
            </div>
            <div class="tree-item">
              <img src="../../public/imgs/aboutme/skill-tree/server.png" alt="后端开发">
              <p>后端开发</p>
            </div>
            <div class="skill-list">
              <div
                v-for="(skill, index) in myScoreConfig.server"
                :key="index"
                class="skill-item"
              >
                <div class="skill-ring">
                  <svg viewBox="0 0 120 120">
                    <circle class="ring-bg" cx="60" cy="60" r="52" />
                    <circle
                      class="ring-progress"
                      cx="60" cy="60" r="52"
                      :style="{
                        strokeDashoffset: 327 * (1 - skill.score / 100),
                        stroke: skill.backcolor || '#1677ff'
                      }"
                    />
                  </svg>
                  <span class="ring-name">{{ skill.name }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {onMounted, onUnmounted} from 'vue'

const myScoreConfig = {
  web:[
    {
      name:'HTML',
      score:5,
      backcolor:''
    },{
      name:'HTML',
      score:5,
      backcolor:''
    },{
      name:'HTML',
      score:5,
      backcolor:''
    },{
      name:'HTML',
      score:5,
      backcolor:''
    },{
      name:'HTML',
      score:5,
      backcolor:''
    },{
      name:'HTML',
      score:5,
      backcolor:''
    }
  ],
  server:[

  ]
}

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

    .resume-box {
      margin: 0 0 0 10px;
      flex: 7;

      .skill-treee {
        padding: 20px;

        .tree-message {

          .tree-item {
            padding: 20px 0;
            display: flex;

            img {
              margin: 1px 0 0 0;
              margin-right: 20px;
              width: 18px;
              height: 16px;
            }

            p {
              line-height: 18px;
              font-size: 18px;
            }
          }

          .skill-list {
            display: flex;
            flex-direction: column;
            flex-wrap: wrap;

            .skill {
              padding: 16px;
              border-radius: 16px;
              color: white;
            }
          }
        }
      }
    }
  }
}
</style>
