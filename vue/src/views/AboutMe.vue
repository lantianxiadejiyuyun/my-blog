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
              <img src="../../public/imgs/aboutme/github.svg" alt="GitHub" width="20" height="20">
              <p>Github</p>
            </a>
            <a class="tel-item" href="mailto:your@email.com" title="Email">
              <img src="../../public/imgs/aboutme/email.svg" alt="Email" width="20" height="20">
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
              <div class="skill" v-for="(item,i) in myScoreConfig.web" :key="i">
                <p :style="{ color: item.color }">
                  {{ item.name }}
                </p>
                <div class="back"
                     :style="{ width: getSkillBackWidth(item.score), backgroundColor: item.backcolor }"></div>
              </div>
            </div>

            <div class="tree-item">
              <img src="../../public/imgs/aboutme/skill-tree/server.png" alt="后端开发">
              <p>后端开发</p>
            </div>

            <div class="skill-list">
              <div class="skill" v-for="(item,i) in myScoreConfig.server" :key="i">
                <p :style="{ color: item.color }">
                  {{ item.name }}
                </p>
                <div class="back"
                     :style="{ width: getSkillBackWidth(item.score), backgroundColor: item.backcolor }"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="introduction box">
          <div class="title">
            履历
          </div>
          <div class="timeline">
            <div class="timeline-item">
              <div class="timeline-dot"></div>
              <div class="timeline-content">
                <h3>2024 - 至今</h3>
                <p>某公司 前端开发工程师</p>
              </div>
            </div>
            <div class="timeline-item">
              <div class="timeline-dot"></div>
              <div class="timeline-content">
                <h3>2020 - 2024</h3>
                <p>某大学 计算机科学专业</p>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {computed, onMounted, onUnmounted, ref} from 'vue'

const myScoreConfig = ref({
  web: [
    {
      name: 'HTML',
      score: 5,
      backcolor: '#a8d8ff',
      color: '#1a73ab',
    }, {
      name: 'CSS',
      score: 4,
      backcolor: '#a8e6cf',
      color: '#2e7d5b',
    }, {
      name: 'JavaScript',
      score: 4,
      backcolor: '#ffe0a8',
      color: '#b8860b',
    }, {
      name: 'Vue',
      score: 4,
      backcolor: '#c8b6ff',
      color: '#6a4fc9',
    }, {
      name: 'TypeScript',
      score: 3,
      backcolor: '#b8e0ff',
      color: '#1a6fa8',
    }, {
      name: 'Node.js',
      score: 3,
      backcolor: '#b5ead7',
      color: '#2b7a5f',
    }
  ],
  server: [
    {
      name: 'Python',
      score: 4,
      backcolor: '#ffccb8',
      color: '#c45a32',
    }
  ]
})

const getSkillBackWidth = ((score: number) => {
  return (score / 10 * 100) + '%'
})

onMounted(() => {
})

onUnmounted(() => {

})
</script>

<style lang="scss" scoped>
.content {
  position: relative;

  .header-box {
    position: relative;
    background: url("../../public/imgs/aboutme/top-back.png");
    background-size: cover;
    height: 40vh;
  }

  .header-box::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(to bottom, transparent, #fff);
  }

  .main {
    top: -10vh;
    position: relative;
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

        .title {
          font-size: 22px;
          font-weight: 600;
        }

        .tree-message {

          .skill-list {
            display: flex;
            flex-direction: column;

            .skill {
              margin-bottom: 10px;
              padding: 20px;
              border-radius: 10px;
              background-color: #f4f4f4;
              color: #000000;
              border: 1px solid #f0f0f0;
              position: relative;

              p {
                z-index: 20;
                position: relative;
                color: black;
              }

              .back {
                top: 0;
                left: 0;
                position: absolute;
                height: 100%;
                border-radius: 10px;
              }
            }
          }

          .tree-item {
            padding: 20px 0;
            display: flex;
          }

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
      }

      .introduction {
        padding: 24px;

        .title {
          font-size: 22px;
          font-weight: 600;
          margin-bottom: 8px;
        }

        .timeline {
          position: relative;
          padding-left: 30px;

          &::before {
            content: '';
            position: absolute;
            left: 9px;
            top: 4px;
            bottom: 0;
            width: 2px;
            background: #e0e0e0;
          }

          .timeline-item {
            position: relative;
            margin-bottom: 24px;
          }

          .timeline-dot {
            position: absolute;
            left: -26px;
            top: 6px;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #1677ff;
            border: 2px solid #fff;
            box-shadow: 0 0 0 2px #1677ff;
          }

          .timeline-content {
            padding: 16px;
            background: #f9f9f9;
            border-radius: 8px;

            h3 {
              font-size: 15px;
              color: #1677ff;
              margin-bottom: 4px;
            }
          }
        }
      }
    }
  }
}
</style>
