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
        <div class="skill-tree box">
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
                <img class="skill-icon" :src="item.icon" :alt="item.name">
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
                <img class="skill-icon" :src="item.icon" :alt="item.name">
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
            <div class="timeline-item" v-for="(item,i) in myResume" :key="i">
              <div class="timeline-dot"></div>
              <div class="timeline-content">
                <h3>{{ item.time }}</h3>
                <p class="company">{{ item.company }}</p>
                <p class="desc">{{ item.desc }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {onMounted, onUnmounted, ref} from 'vue'

const myScoreConfig = ref({
  web: [
    {
      name: 'HTML',
      score: 9.5,
      backcolor: '#fde8d0',
      color: '#e44d26',
      icon: '../../public/imgs/aboutme/skill-tree/html.svg',
    }, {
      name: 'Vue',
      score: 9,
      backcolor: '#d4f5e2',
      color: '#42b883',
      icon: '../../public/imgs/aboutme/skill-tree/vue.svg',
    }, {
      name: 'CSS',
      score: 8,
      backcolor: '#d0e8fd',
      color: '#264de4',
      icon: '../../public/imgs/aboutme/skill-tree/css.svg',
    }, {
      name: 'JavaScript',
      score: 8,
      backcolor: '#fdf6d0',
      color: '#b8860b',
      icon: '../../public/imgs/aboutme/skill-tree/javascript.svg',
    }, {
      name: 'Uniapp',
      score: 8,
      backcolor: '#e2d4f5',
      color: '#6a4fc9',
      icon: '../../public/imgs/aboutme/skill-tree/uniapp.svg',
    }, {
      name: 'TypeScript',
      score: 7,
      backcolor: '#d0e4fd',
      color: '#3178c6',
      icon: '../../public/imgs/aboutme/skill-tree/typescript.svg',
    }
  ],
  server: [
    {
      name: 'Python',
      score: 8,
      backcolor: '#d0f0e8',
      color: '#3776ab',
      icon: '../../public/imgs/aboutme/skill-tree/python.svg',
    }, {
      name: 'Java',
      score: 6,
      backcolor: '#fde8d0',
      color: '#e76f00',
      icon: '../../public/imgs/aboutme/skill-tree/java.svg',
    }, {
      name: 'Node.js',
      score: 6,
      backcolor: '#d4f5d0',
      color: '#339933',
      icon: '../../public/imgs/aboutme/skill-tree/nodejs.svg',
    }
  ]
})

const myResume = ref([
  {
    company: '潍坊三立，全栈开发工程师',
    desc: '负责公司核心业务系统前后端开发，微信小程序开发，uniapp跨端开发，主要技术栈：Vue / TypeScript / Uniapp / Node.js / Python',
    time: '2024.2 - 至今'
  },
  {
    company: '独立工作室，全栈开发工程师',
    desc: '负责前端网站以及跨端app开发（宇宙文学Web端官网，宇宙文学Uniapp开发），主要技术栈：Vue / TypeScript / Uniapp',
    time: '2023.9 - 2023.12'
  },
  {
    company: '潍坊博尧，前端开发工程师',
    desc: '负责客户项目的前端开发与交付（后台管理平台，企业门户网站），主要技术栈：Vue / JavaScript',
    time: '2023.5 - 2023.8'
  }
])

const getSkillBackWidth = ((score: number) => {
  return (score / 10 * 100) + '%'
})

onMounted(() => {
})

onUnmounted(() => {

})
</script>

<style lang="scss" scoped>

@media (max-width: 768px) {
  .content {
    .main {
      flex-direction: column;
      padding: 0 10px;

      .resume-box {
        margin: 0 0 0 0 !important;
      }
    }
  }
}

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

    .resume-box {
      margin: 0 0 0 10px;
      flex: 7;

      .skill-tree {
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
              display: flex;
              align-items: center;

              .skill-icon {
                width: 20px;
                height: 20px;
                margin-right: 10px;
                flex-shrink: 0;
                z-index: 20;
                position: relative;
              }

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

            .company {
              font-size: 14px;
              font-weight: 600;
              color: #333;
              margin-bottom: 6px;
            }

            .desc {
              font-size: 13px;
              color: #666;
              line-height: 1.6;
            }
          }
        }
      }
    }
  }
}
</style>
