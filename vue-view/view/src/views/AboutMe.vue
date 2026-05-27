<template>
  <div class="content">
    <!-- 留一个空间 -->
    <div class="header-box">

    </div>
    <div class="main">
      <!--个人介绍-->
      <div class="introduction-box">
        <AboutMeFlotBar></AboutMeFlotBar>
      </div>
      <!--履历-->
      <div class="resume-box">
        <div class="skill-tree box">
          <div class="title">
            我的技能树
          </div>
          <div class="tree-message">
            <div class="tree-item">
              <img src="/imgs/aboutme/skill-tree/web.png" alt="前端开发">
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
              <img src="/imgs/aboutme/skill-tree/server.png" alt="后端开发">
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
import AboutMeFlotBar from '@/component/AboutMeFlotBar.vue'

import {onMounted, onUnmounted, ref} from 'vue'

const myScoreConfig = ref({
  web: [
    {
      name: 'HTML',
      score: 9.5,
      backcolor: '#fde8d0',
      color: '#e44d26',
      icon: '/imgs/aboutme/skill-tree/html.svg',
    }, {
      name: 'Vue',
      score: 9,
      backcolor: '#d4f5e2',
      color: '#42b883',
      icon: '/imgs/aboutme/skill-tree/vue.svg',
    }, {
      name: 'CSS',
      score: 8,
      backcolor: '#d0e8fd',
      color: '#264de4',
      icon: '/imgs/aboutme/skill-tree/css.svg',
    }, {
      name: 'JavaScript',
      score: 8,
      backcolor: '#fdf6d0',
      color: '#b8860b',
      icon: '/imgs/aboutme/skill-tree/javascript.svg',
    }, {
      name: 'Uniapp',
      score: 8,
      backcolor: '#e2d4f5',
      color: '#6a4fc9',
      icon: '/imgs/aboutme/skill-tree/uniapp.svg',
    }, {
      name: 'TypeScript',
      score: 7,
      backcolor: '#d0e4fd',
      color: '#3178c6',
      icon: '/imgs/aboutme/skill-tree/typescript.svg',
    }
  ],
  server: [
    {
      name: 'Python',
      score: 8,
      backcolor: '#d0f0e8',
      color: '#3776ab',
      icon: '/imgs/aboutme/skill-tree/python.svg',
    }, {
      name: 'Java',
      score: 6,
      backcolor: '#fde8d0',
      color: '#e76f00',
      icon: '/imgs/aboutme/skill-tree/java.svg',
    }, {
      name: 'Node.js',
      score: 6,
      backcolor: '#d4f5d0',
      color: '#339933',
      icon: '/imgs/aboutme/skill-tree/nodejs.svg',
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
    background: url("/imgs/aboutme/top-back.png");
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
    background: linear-gradient(to bottom, transparent, var(--bg-primary));
  }

  .main {
    top: -10vh;
    position: relative;
    min-height: 100vh;

    display: flex;
    justify-content: space-between;

    .introduction-box {
      flex: 3;
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
              background-color: var(--bg-tertiary);
              color: var(--font-size-color);
              border: 1px solid var(--border-color);
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
                color: var(--font-size-color);
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
            background: var(--border-light);
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
            background: var(--color-primary);
            border: 2px solid var(--bg-primary);
            box-shadow: 0 0 0 2px var(--color-primary);
          }

          .timeline-content {
            padding: 16px;
            background: var(--bg-tertiary);
            border-radius: 8px;

            h3 {
              font-size: 15px;
              color: var(--color-primary);
              margin-bottom: 4px;
            }

            .company {
              font-size: 14px;
              font-weight: 600;
              color: var(--text-primary);
              margin-bottom: 6px;
            }

            .desc {
              font-size: 13px;
              color: var(--text-secondary);
              line-height: 1.6;
            }
          }
        }
      }
    }
  }
}
</style>
