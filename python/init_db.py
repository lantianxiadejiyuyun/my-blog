"""
初始化数据库并写入大量假数据（约 25 篇文章、60+ 评论）
使用方法：python init_db.py
"""
import sys
from datetime import datetime, timedelta
from random import randint, choice, random

from dotenv import load_dotenv
load_dotenv(override=True)

import bcrypt

from app import create_app
from app.extensions import db
from app.models import User, Article, Category, Tag, Comment, FriendLink, Carousel


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def seed():
    app = create_app()

    with app.app_context():
        # 清空
        print('重建所有表...')
        db.drop_all()
        db.create_all()
        print('已重建，ID 已重置。\n')

        # ============================================
        # 1. 用户
        # ============================================
        print('创建用户...')
        users_data = [
            ('admin',  'admin123',   'admin@blog.com',     '博客管理员，全栈工程师',           'admin'),
            ('eugen',  '123456',     'eugen@blog.com',     '全栈开发，Python & Vue 爱好者',   'admin'),
            ('alice',  '123456',     'alice@example.com',  '前端开发者，React / TypeScript',   'user'),
            ('bob',    '123456',     'bob@example.com',    'DevOps 工程师，K8s 布道者',        'user'),
            ('charlie','123456',     'charlie@dev.io',     'Golang 后端，兼修 Rust',           'user'),
            ('diana',  '123456',     'diana@dev.io',       '数据工程师，ML 炼丹师',             'user'),
            ('eric',   '123456',     'eric@dev.io',        '安全工程师，CTF 选手',              'user'),
            ('fiona',  '123456',     'fiona@dev.io',       '移动端开发，Flutter 爱好者',        'user'),
            ('guest',  'guest',      'guest@example.com',  '我只是一个访客',                    'user', 0),
        ]

        users = {}
        for args in users_data:
            username, pwd, email, bio, role = args[0], args[1], args[2], args[3], args[4]
            status = args[5] if len(args) > 5 else 1
            u = User(
                username=username,
                password=hash_password(pwd),
                email=email,
                avatar=f'https://api.dicebear.com/8.x/initials/svg?seed={username}',
                bio=bio,
                role=role,
                status=status,
            )
            db.session.add(u)
            users[username] = u
        db.session.commit()
        print(f'  ✓ {len(users)} 个用户')

        # ============================================
        # 2. 分类
        # ============================================
        print('创建分类...')
        cats_data = [
            ('Python',     'Python 语言、框架、数据分析'),
            ('JavaScript', '前端开发、Node.js、框架生态'),
            ('DevOps',     'CI/CD、容器、监控、云原生'),
            ('数据库',     'MySQL/Redis/Mongo/PostgreSQL'),
            ('Golang',     'Go 语言后端开发与高性能编程'),
            ('安全',       'Web 安全、渗透测试、密码学'),
            ('杂谈',       '技术感悟、效率工具、职业发展'),
        ]
        categories = []
        for name, desc in cats_data:
            c = Category(name=name, description=desc)
            db.session.add(c)
            categories.append(c)
        db.session.commit()
        print(f'  ✓ {len(categories)} 个分类')

        # ============================================
        # 3. 标签
        # ============================================
        print('创建标签...')
        tag_names = [
            'Flask', 'Django', 'FastAPI', 'Vue', 'React', 'Angular',
            'Docker', 'Kubernetes', 'MySQL', 'Redis', 'MongoDB', 'PostgreSQL',
            'Linux', 'Git', 'RESTful', 'GraphQL', 'Webpack', 'Vite',
            'TypeScript', 'Nginx', 'CI/CD', '算法', '设计模式', '微服务',
            'WebSocket', 'gRPC', 'Serverless', 'Terraform', 'Prometheus', 'ELK',
        ]
        tags = []
        for name in tag_names:
            t = Tag(name=name)
            db.session.add(t)
            tags.append(t)
        db.session.commit()
        print(f'  ✓ {len(tags)} 个标签')

        # ============================================
        # 4. 文章 (25 篇)
        # ============================================
        print('创建文章...')

        A = articles_data = []

        def mk(title, summary, content, cat_idx, author_name, tag_idxs, status=1, views=None):
            if views is None:
                views = randint(200, 8000)
            return {
                'title': title, 'summary': summary, 'content': content,
                'category_index': cat_idx, 'author': users[author_name],
                'tag_indices': tag_idxs, 'status': status, 'view_count': views,
            }

        # ---- Python ----
        A.append(mk(
            'Flask 项目结构最佳实践',
            '介绍 Flask 项目的目录结构设计思路和工厂函数模式的好处',
            """## 前言

Flask 是一个轻量级的 Python Web 框架，但项目变大后需要合理的目录结构。

## 推荐结构

```
project/
├── app/
│   ├── __init__.py      # 工厂函数
│   ├── config.py        # 配置类
│   ├── extensions.py    # 插件初始化
│   ├── models.py        # 数据模型
│   ├── errors.py        # 错误处理
│   └── public/          # 蓝图模块
├── .env
├── main.py
└── requirements.txt
```

## 为什么要用工厂函数？

1. **延迟初始化** — app 在运行时才创建，扩展在 init_app 时才绑定
2. **测试友好** — 每个测试可以创建独立的 app 实例
3. **多环境** — 可以根据配置创建不同环境的 app

## 总结

良好的项目结构是项目可维护性的基础，从一开始就规范起来！""",
            0, 'eugen', [0, 13, 14], views=1523),
        )

        A.append(mk(
            'FastAPI vs Flask：该怎么选？',
            '从性能、异步支持、生态等角度对比两个流行 Python Web 框架',
            """## 背景

Python Web 框架中，Flask 是老牌轻量选手，FastAPI 是近年新秀。到底该选哪个？

## 性能对比

FastAPI 基于 Starlette + Pydantic，原生异步支持，性能远超 Flask。

| 框架 | 请求/秒 | 异步支持 |
|------|--------|---------|
| Flask | ~5,000 | 需插件 |
| FastAPI | ~30,000 | 原生 |

## 生态系统

- Flask 生态成熟，插件丰富（Flask-SQLAlchemy、Flask-Login……）
- FastAPI 依赖 Starlette 生态，但也能复用部分 Flask 生态

## 我的建议

- 快速原型 / 简单 CRUD → Flask
- 高并发 API / 微服务 → FastAPI
- 大型项目 → Django 更合适

选型要结合团队能力和项目需求，不要盲目追新。""",
            0, 'charlie', [2, 0, 1, 14], views=3420),
        )

        A.append(mk(
            'Python 异步编程：从回调到 async/await',
            '一文搞懂 Python 异步编程的演进历程和核心概念',
            """## 同步 vs 异步

同步代码一行一行执行，遇到 I/O 就阻塞。异步代码可以在 I/O 等待时切换到其他任务。

## 演进历程

### 回调时期
```python
def fetch(url, callback):
    ...
    callback(data)
```
回调地狱，难以维护。

### Future / Promise
```python
future = executor.submit(task)
result = future.result(timeout=5)
```
好了一些，但还是不够直观。

### async/await (Python 3.5+)
```python
async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()
```
这才是现代 Python 异步编程该有的样子！

## 关键概念

- **event loop** — 事件循环，调度的核心
- **coroutine** — 协程，可以暂停和恢复的函数
- **Task** — 对协程的包装，并发执行

## 注意事项

1. 不要在协程里调用同步阻塞函数
2. CPU 密集型任务要用 `run_in_executor`
3. 数据库驱动也要用异步版本（如 aiomysql）

掌握异步，Python 性能提升一个台阶！""",
            0, 'eugen', [0, 2, 14], views=2890),
        )

        A.append(mk(
            'Django REST Framework 快速上手',
            '使用 DRF 构建 RESTful API 的完整教程',
            """## 安装

```bash
pip install djangorestframework
```

## Serializer — 序列化层

```python
from rest_framework import serializers

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
```

## ViewSet — 视图层

```python
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
```

## Router — 路由层

```python
router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
```

三行代码搞定 CRUD！Django REST Framework 就是这样高效。""",
            0, 'alice', [1, 14], views=1870),
        )

        # ---- JavaScript ----
        A.append(mk(
            'React Hooks 进阶：useMemo 和 useCallback',
            '深入理解 React 性能优化的两个核心 Hook',
            """## 为什么需要 useMemo 和 useCallback

React 每次渲染都会重新创建函数和计算值，当传给子组件时可能导致不必要的重渲染。

## useMemo — 缓存计算结果

```jsx
const sortedList = useMemo(() => {
    return items.sort((a, b) => a.name.localeCompare(b.name));
}, [items]);  // 只有 items 变了才重新排序
```

## useCallback — 缓存函数引用

```jsx
const handleClick = useCallback((id) => {
    setSelected(id);
}, []);  // 函数引用保持不变
```

## 注意事项

1. 不要到处乱加 — 缓存本身也有开销
2. 只在传递给 `React.memo` 子组件时才需要 useCallback
3. 依赖数组要写对，否则缓存失效

合理使用这两个 Hook，React 应用的性能会好很多！""",
            1, 'alice', [4, 17, 18], views=4100),
        )

        A.append(mk(
            'TypeScript 高级类型体操',
            '泛型、条件类型、映射类型 —— 让你的 TS 代码更优雅',
            """## 泛型

```typescript
function first<T>(arr: T[]): T | undefined {
    return arr[0];
}
```

## 条件类型

```typescript
type IsString<T> = T extends string ? true : false;
type A = IsString<'hello'>;  // true
type B = IsString<42>;       // false
```

## 映射类型

```typescript
type Readonly<T> = {
    readonly [K in keyof T]: T[K];
};
```

## 实际应用：API 响应类型

```typescript
type ApiResponse<T> = {
    code: number;
    data: T;
    message: string;
};

type ArticleList = ApiResponse<Article[]>;
```

TypeScript 的类型系统是图灵完备的，越深入越有趣！""",
            1, 'alice', [18, 2, 4], views=2670),
        )

        A.append(mk(
            'Vue 3 Composition API 实战',
            '用组合式 API 重构你的 Vue 项目',
            """## 为什么选择 Composition API

Options API 在组件变大时，逻辑分散在不同选项中，难以维护。

Composition API 把相关逻辑放在一起：

```vue
<script setup>
import { ref, computed, onMounted } from 'vue';

const posts = ref([]);
const loading = ref(false);

const publishedPosts = computed(() =>
    posts.value.filter(p => p.status === 1)
);

onMounted(async () => {
    loading.value = true;
    posts.value = await fetchPosts();
    loading.value = false;
});
</script>
```

## 自定义 Composable

```js
// useCounter.js
export function useCounter(initial = 0) {
    const count = ref(initial);
    const inc = () => count.value++;
    const dec = () => count.value--;
    return { count, inc, dec };
}
```

组合式 API 让代码复用达到新高度！""",
            1, 'eugen', [3, 18, 14], views=5300),
        )

        A.append(mk(
            '从 Webpack 迁移到 Vite：开发体验翻倍',
            '告别漫长的冷启动，拥抱 Vite 的极速开发体验',
            """## 为什么迁移

一个中等规模的项目，Webpack 冷启动可能要 30 秒+，Vite 只需 1 秒。

## Vite 为什么快

Vite 利用浏览器原生 ES Module：
- 开发时：按需编译，只编译当前页面用到的模块
- 构建时：用 Rollup 打包，输出高度优化

## 迁移步骤

```bash
npm uninstall webpack webpack-cli webpack-dev-server
npm install -D vite @vitejs/plugin-vue
```

```js
// vite.config.js
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
    plugins: [vue()],
    server: { port: 3000 },
});
```

迁移过程比想象中简单，花一个下午就够！""",
            1, 'alice', [17, 3, 4], views=3450),
        )

        # ---- DevOps ----
        A.append(mk(
            '用 Docker 部署你的第一个 Flask 应用',
            '从零开始，用 Docker 容器化部署 Flask 应用',
            """## 为什么用 Docker

Docker 让部署变得简单、可靠、可复现。不再有"在我机器上能跑"的问题。

## Dockerfile

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "main.py"]
```

## docker-compose.yml

```yaml
services:
  app:
    build: .
    ports: ["5000:5000"]
    depends_on: [mysql, redis]
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: blog
  redis:
    image: redis:7-alpine
```

一行 `docker-compose up -d` 全部搞定！""",
            2, 'eugen', [0, 6, 19], views=4100),
        )

        A.append(mk(
            'Kubernetes 入门：从 Pod 到 Deployment',
            'K8s 核心概念详解，带你迈出容器编排第一步',
            """## 容器编排是什么

单机 Docker 适合开发和小项目，生产环境需要：
- 自动扩缩容
- 服务发现
- 滚动更新
- 自愈能力

Kubernetes 就是做这些的。

## 核心概念

### Pod
最小的调度单元，包含一个或多个容器。

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
spec:
  containers:
  - name: app
    image: my-app:latest
```

### Deployment
管理 Pod 的声明式更新。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    # Pod template...
```

## 总结

K8s 学习曲线陡峭，但掌握后运维效率质的飞跃！""",
            2, 'bob', [7, 6, 27], views=6700),
        )

        A.append(mk(
            'GitHub Actions 自动化部署指南',
            '配置 CI/CD 流水线，代码推送即自动部署',
            """## 什么是 CI/CD

- **CI（持续集成）**：代码合并后自动构建、测试
- **CD（持续部署）**：测试通过后自动部署

## GitHub Actions 配置

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build & Push
        run: |
          docker build -t my-app .
          docker push my-app
      - name: Deploy
        run: |
          ssh server 'docker pull my-app && docker-compose up -d'
```

## 好处

- 每次推送自动触发，不用手动部署
- 构建历史可追溯
- 失败自动通知

免费额度足够个人项目使用，强烈推荐！""",
            2, 'bob', [13, 6, 14], views=2340),
        )

        A.append(mk(
            'Nginx 反向代理和负载均衡',
            '用 Nginx 为你的应用加速，轻松处理高并发',
            """## 反向代理

```nginx
server {
    listen 80;
    server_name blog.example.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 负载均衡

```nginx
upstream backend {
    server 192.168.1.10:5000 weight=3;
    server 192.168.1.11:5000;
    server 192.168.1.12:5000 backup;
}

server {
    location / {
        proxy_pass http://backend;
    }
}
```

## HTTPS 配置

```nginx
server {
    listen 443 ssl;
    ssl_certificate     /etc/ssl/cert.pem;
    ssl_certificate_key /etc/ssl/key.pem;
    ...
}
```

用 certbot 自动申请 Let's Encrypt 免费证书：

```bash
certbot --nginx -d blog.example.com
```

Nginx 是前端的守门人，每个后端工程师都应该会配。""",
            2, 'bob', [19, 13, 7], views=3890),
        )

        A.append(mk(
            'Prometheus + Grafana 监控体系搭建',
            '为你的服务加上可观测性，出问题第一时间知道',
            """## 监控什么

- **基础设施**：CPU、内存、磁盘、网络
- **应用**：QPS、延迟、错误率
- **业务**：注册量、订单量、DAU

## Prometheus

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'my-app'
    static_configs:
      - targets: ['localhost:5000']
```

## Grafana

导入社区 Dashboard，几分钟就能有漂亮的监控面板。

常用的 Dashboard ID：
- Node Exporter: 1860
- MySQL: 7362
- Redis: 763
- Flask 应用: 自定义

## 黄金信号

每个服务都应该监控这 4 个指标：
1. **延迟** — 请求耗时
2. **流量** — QPS
3. **错误** — 错误率
4. **饱和度** — 资源使用率

出问题了也按这 4 个维度排查。""",
            2, 'bob', [28, 7, 6], views=1560),
        )

        # ---- 数据库 ----
        A.append(mk(
            'MySQL 索引优化实战',
            '深入理解 MySQL 索引原理，学会用 EXPLAIN 分析查询',
            """## 为什么索引很重要

没有索引时全表扫描；有合适索引，查询速度提升 N 个数量级。

## 索引类型

### B+Tree（默认）
```sql
CREATE INDEX idx_username ON user(username);
```

### 联合索引 — 最左前缀原则

联合索引 `(A, B, C)`：
- `WHERE A = ?`  ✓
- `WHERE A = ? AND B = ?`  ✓
- `WHERE B = ?`  ✗  (跳过了 A)

## EXPLAIN

```sql
EXPLAIN SELECT * FROM articles WHERE category_id = 1 AND status = 1;
```

`type` 字段从好到差：
const → ref → range → index → ALL

## 总结

建索引不难，建对才难。为查询条件建索引，用 EXPLAIN 验证！""",
            3, 'eugen', [8, 12], views=6200),
        )

        A.append(mk(
            'Redis 缓存策略全解析',
            '缓存穿透、击穿、雪崩 —— 一套方案全解决',
            """## 缓存问题三兄弟

### 缓存穿透
查不存在的数据，缓存层空，请求直接打到 DB。
**解决**：布隆过滤器 / 缓存空值（短期）

### 缓存击穿
热点 key 过期瞬间，大量请求打到 DB。
**解决**：互斥锁 / 逻辑过期 / 永不过期 + 异步更新

### 缓存雪崩
大量 key 同时过期，DB 瞬间压力过大。
**解决**：过期时间加随机值 / 多级缓存 / 限流降级

## 代码示例

```python
data = cache.get(key)
if data is None:
    # 加锁防止击穿
    lock_key = f'lock:{key}'
    if cache.setnx(lock_key, 1):
        data = db.query(...)
        cache.set(key, data, ttl + random.randint(0, 300))
        cache.delete(lock_key)
```

三种问题本质都是"缓存没挡住"，理解原理最重要。""",
            3, 'bob', [9, 8, 12], views=4980),
        )

        A.append(mk(
            'PostgreSQL 的 JSON 查询技巧',
            '利用 PostgreSQL 强大的 JSON 支持，灵活存储半结构化数据',
            """## JSON vs JSONB

PostgreSQL 提供两种 JSON 类型：
- **JSON**：纯文本存储，保留格式和顺序
- **JSONB**：二进制存储，支持索引，推荐使用

## 常用操作

```sql
-- 查询 JSON 字段
SELECT data->'name' FROM users;

-- 按 JSON 内的值过滤
SELECT * FROM articles WHERE metadata->>'lang' = 'zh';

-- 更新 JSON 内的值
UPDATE users SET data = jsonb_set(data, '{age}', '26');

-- JSON 数组展开
SELECT jsonb_array_elements(tags) FROM articles;
```

## GIN 索引

```sql
CREATE INDEX idx_metadata ON articles USING GIN (metadata);
```

有了 GIN 索引，JSON 查询也能飞快！""",
            3, 'diana', [11, 12, 8], views=1750),
        )

        A.append(mk(
            'MongoDB 入门：文档型数据库的正确用法',
            '什么时候该用 MongoDB，什么时候不该用',
            """## MongoDB 的特点

- Schema-less，结构灵活
- JSON 文档存储，和代码数据结构一致
- 水平扩展方便

## 适用场景

✅ 日志存储
✅ 爬虫数据
✅ 用户画像
✅ IoT 时序数据
✅ 内容管理系统

## 不适用场景

❌ 复杂事务
❌ 多表关联查询
❌ 强一致性要求

## 基本操作

```javascript
// 插入
db.articles.insertOne({ title: "Hello", views: 100 });

// 查询
db.articles.find({ views: { $gt: 50 } }).sort({ views: -1 });

// 聚合
db.articles.aggregate([
    { $group: { _id: "$category", count: { $sum: 1 } } }
]);
```

MongoDB 是好工具，但不要当关系型数据库用。""",
            3, 'diana', [10, 8, 12], views=2100),
        )

        # ---- Golang ----
        A.append(mk(
            'Go 语言并发编程：Goroutine 和 Channel',
            '掌握 Go 最强大的武器 —— 轻量级并发',
            """## Goroutine

Go 的并发哲学：不要通过共享内存来通信，而要通过通信来共享内存。

```go
go func() {
    fmt.Println("Hello from goroutine!")
}()
```

一个 Go 程序可以轻松跑几十万个 goroutine，每个只占几 KB。

## Channel

```go
ch := make(chan string)

go func() {
    ch <- "hello"  // 发送
}()

msg := <-ch  // 接收
fmt.Println(msg)
```

## Select

```go
select {
case msg := <-ch1:
    fmt.Println("from ch1:", msg)
case msg := <-ch2:
    fmt.Println("from ch2:", msg)
case <-time.After(1 * time.Second):
    fmt.Println("timeout")
}
```

## 实际应用

```go
func fetchAll(urls []string) []Response {
    ch := make(chan Response, len(urls))
    for _, url := range urls {
        go func(u string) {
            ch <- fetch(u)
        }(url)
    }
    // collect results...
}
```

并发是 Go 的杀手级特性，学会它就掌握了 Go 的核心！""",
            4, 'charlie', [25, 14, 22], views=4300),
        )

        A.append(mk(
            '用 Gin 构建 RESTful API',
            'Go 语言最流行的 Web 框架 Gin 实战教程',
            """## 为什么选 Gin

Gin 是目前 Go 生态最流行的 Web 框架：
- 性能极高（比 Flask/Express 快 10x+）
- API 简洁优雅
- 中间件生态丰富

## Hello World

```go
package main

import "github.com/gin-gonic/gin"

func main() {
    r := gin.Default()
    r.GET("/ping", func(c *gin.Context) {
        c.JSON(200, gin.H{"message": "pong"})
    })
    r.Run(":8080")
}
```

## 分组路由

```go
api := r.Group("/api")
{
    api.GET("/articles", listArticles)
    api.GET("/articles/:id", getArticle)
    api.POST("/articles", createArticle)
}
```

## 中间件

```go
func AuthMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        token := c.GetHeader("Authorization")
        // ...验证逻辑
        c.Next()
    }
}
```

Go + Gin = 高性能 API 的黄金组合！""",
            4, 'charlie', [14, 25], views=2900),
        )

        A.append(mk(
            'Go 语言错误处理的最佳实践',
            '告别 if err != nil 地狱，写出优雅的 Go 错误处理代码',
            """## Go 的错误哲学

Go 不使用异常，而是将错误作为返回值：

```go
f, err := os.Open("file.txt")
if err != nil {
    return fmt.Errorf("打开文件失败: %w", err)
}
defer f.Close()
```

## 错误包装

Go 1.13+ 支持错误包装：

```go
// 包装错误，保留原始信息
err := fmt.Errorf("查询用户失败: %w", sqlErr)

// 判断错误类型
if errors.Is(err, sql.ErrNoRows) { ... }

// 提取错误类型
var notFound *NotFoundError
if errors.As(err, &notFound) { ... }
```

## 自定义错误类型

```go
type ValidationError struct {
    Field string
    Value interface{}
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("字段 %s 的值 %v 不合法", e.Field, e.Value)
}
```

## 总结

Go 的错误处理虽然啰嗦，但让错误路径显式化，这正是 Go 的设计哲学。""",
            4, 'charlie', [14, 22], views=1850),
        )

        # ---- 安全 ----
        A.append(mk(
            'Web 常见安全漏洞及防御方案',
            'XSS、CSRF、SQL 注入 —— 每个 Web 开发者都应该了解的安全知识',
            """## 1. XSS（跨站脚本攻击）

攻击者在页面注入恶意脚本。

**防御**：
- 输出时 HTML 转义
- Content-Security-Policy 头
- HttpOnly Cookie

## 2. CSRF（跨站请求伪造）

诱导用户点击链接，利用登录态发起恶意请求。

**防御**：
- CSRF Token
- SameSite Cookie
- 验证 Referer

## 3. SQL 注入

```python
# ❌ 危险！
cursor.execute(f"SELECT * FROM user WHERE id = {user_id}")

# ✅ 安全
cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,))
```

## 4. 密码存储

```python
# ❌ 永远不要明文存储！
# ❌ 不要用 MD5/SHA1！

# ✅ 用 bcrypt
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

安全不是某个人的事，是每个开发者的责任。""",
            5, 'eric', [8, 13, 14], views=7200),
        )

        A.append(mk(
            'JWT 认证机制深入理解',
            'Token 是怎么工作的？Access Token 和 Refresh Token 的区别',
            """## 什么是 JWT

JWT（JSON Web Token）由三部分组成（用 `.` 分隔）：
- **Header**：算法信息
- **Payload**：用户数据（不要存敏感信息！）
- **Signature**：签名，防篡改

## 工作流程

```
用户登录 → 服务端验证 → 返回 Token
→ 前端存储 Token → 每次请求带上
→ 服务端验证 Token → 返回数据
```

## Access Token vs Refresh Token

| | Access Token | Refresh Token |
|---|---|---|
| 有效期 | 短（15分钟~2小时） | 长（7~30天） |
| 存储位置 | 内存 | HttpOnly Cookie |
| 作用 | 访问API | 刷新Access Token |

## 实践建议

1. Access Token 放在内存，Refresh Token 放 HttpOnly Cookie
2. Token 过期后静默刷新，用户无感知
3. 服务端维护 Token 黑名单，支持主动登出

JWT 不是银弹，简单场景用 Session 也可以。""",
            5, 'eric', [14, 13, 1], views=3100),
        )

        A.append(mk(
            'HTTPS 和 TLS 原理简析',
            '从握手到加密，理解 HTTPS 如何保护你的数据',
            """## 为什么需要 HTTPS

HTTP 明文传输，中间人可以：
- 窃听内容
- 篡改数据
- 冒充身份

HTTPS = HTTP + TLS 加密层。

## TLS 握手过程

1. Client Hello → 支持的加密套件
2. Server Hello → 选定加密套件 + 证书
3. 客户端验证证书
4. 密钥交换（DH/ECDHE）
5. 对称加密通信

## 证书链

```
根证书（Root CA）
  └── 中间证书（Intermediate CA）
       └── 你的证书（Server Cert）
```

浏览器内置了根证书，逐级验证。

## 部署建议

- 用 Let's Encrypt 免费证书
- 强制 HSTS
- 启用 TLS 1.3
- 禁用不安全的加密套件

HTTPS 已经是 Web 的标配，没理由不用！""",
            5, 'eric', [19, 12, 13], views=1900),
        )

        # ---- 杂谈 ----
        A.append(mk(
            '打造个人博客的技术选型之路',
            '分享搭建个人博客的技术选型思路和架构设计',
            """## 技术选型

- **后端**：Flask（轻量灵活）
- **数据库**：MySQL + Redis
- **前端**：Vue 3（Composition API）
- **部署**：Docker + Nginx + GitHub Actions

## 架构图

```
浏览器 → Nginx → Flask API → MySQL
                           → Redis
```

## 为什么不选 Django / Next.js / 其他？

Django 太重型，Next.js 需要学整套全栈范式。Flask + Vue 各司其职，前后端分离清晰。

## 写在最后

技术选型没有标准答案，适合自己就是最好的。先跑起来，再慢慢优化！""",
            6, 'eugen', [0, 3, 8, 9, 19], views=8900),
        )

        A.append(mk(
            '程序员如何高效学习和成长',
            '分享我的学习方法论，帮你少走弯路',
            """## 学习金字塔

被动学习：听讲 → 阅读 → 视听（记忆留存 5%-30%）
主动学习：讨论 → 实践 → **教给别人**（记忆留存 50%-90%）

最高效的学习方式就是**输出倒逼输入**：
- 写博客
- 做开源
- 内部分享

## 我的学习流程

1. **快速概览**：看官方文档的 Quick Start，建立全局认知
2. **实践驱动**：带着项目学，用到什么学什么
3. **深入原理**：读源码、看 RFC、理解设计思想
4. **输出巩固**：写博客、录视频、做分享

## 保持动力的秘诀

- 设定小目标，持续获得正反馈
- 加入技术社区，找到同路人
- 不要和他人比较，和昨天的自己比

学习是一场马拉松，不是百米冲刺。""",
            6, 'eugen', [14, 22, 26], views=10500),
        )

        A.append(mk(
            '我的开发环境配置分享',
            '效率翻倍：终端、编辑器、Chrome 插件推荐',
            """## 终端

- **Windows Terminal** + Oh My Posh 主题
- 包管理：Chocolatey / Scoop

## VS Code 插件

| 插件 | 用途 |
|------|------|
| GitHub Copilot | AI 辅助编程 |
| Prettier | 代码格式化 |
| GitLens | Git 增强 |
| Thunder Client | API 测试 |
| Better Comments | 注释高亮 |

## Chrome 开发插件

- React Developer Tools
- Vue Devtools
- JSON Viewer
- Wappalyzer（识别网站技术栈）

## 效率工具

- **Everything**：Windows 秒搜文件
- **Snipaste**：截图+贴图
- **Obsidian**：笔记管理

好的工具让编码体验完全不同，值得花时间打磨！""",
            6, 'alice', [4, 3, 14], views=5600),
        )

        # 2 篇草稿
        A.append(mk(
            'Python 3.13 新特性速览（草稿）',
            'GIL 改进、更好的错误信息 —— 来看看新版本有什么变化',
            """这篇文章还在写，预计下周发布。主要会介绍：

1. GIL 的可选化进展
2. 错误信息的改进
3. 性能优化部分
4. 新的标准库模块

敬请期待！""",
            0, 'eugen', [0], status=0, views=0),
        )

        A.append(mk(
            '微服务架构设计笔记（草稿）',
            '记录微服务学习过程中的思考和实践',
            """## 为什么这篇是草稿

微服务话题太大，需要更多实践经验才能写出一篇好文章。

目前的笔记要点：
- 服务拆分原则
- 通信方式选择
- 分布式事务处理
- 可观测性建设

先跑一段时间微服务项目再回来补充。""",
            2, 'bob', [23, 7, 25, 28], status=0, views=0),
        )

        # 创建文章对象
        articles = []
        for data in A:
            article = Article(
                title=data['title'],
                content=data['content'],
                summary=data['summary'],
                category=categories[data['category_index']],
                author=data['author'],
                status=data['status'],
                view_count=data.get('view_count', 0),
            )
            for idx in data.get('tag_indices', []):
                article.tags.append(tags[idx])
            db.session.add(article)
            articles.append(article)

        db.session.commit()
        print(f'  ✓ {len(articles)} 篇文章（含 {sum(1 for a in articles if a.status==0)} 篇草稿）')

        # ============================================
        # 5. 评论
        # ============================================
        print('创建评论...')

        comment_pool = [
            '讲得很清楚，收藏了！',
            '看了三遍终于理解了，谢谢博主 🙏',
            '请问有配套的代码仓库吗？',
            '写得不错，不过XXX部分可以再展开一下',
            '和我的项目需求一模一样，太及时了',
            '新手表示看懂了，感谢！',
            '能不能出一篇关于XXX的？很期待',
            '这个方案在生产环境跑过吗？稳定性如何？',
            '补充一个点：还可以用XXX方案替代',
            '感觉比官方文档还容易理解 😂',
            '请问博主一般在哪里交流？想加个微信',
            '我们公司也在用这个技术栈，确实很香',
            '有没有性能测试数据对比？',
            '我之前也遇到过类似的问题，后来用XXX解决了',
            '好文！转发了',
            '为什么不用XXX呢？感觉更轻量',
            '这里有个小错误：XXX应该是YYY才对',
            '博主什么时候更新下一期？',
            '有没有推荐的进阶学习资料？',
            '已经照着教程跑通了，感谢！',
            '确实，理论和实践差别太大了',
            '可以加一个错误处理的章节吗？',
            '这是我看过最好的XXX教程',
            '后端转前端表示学到了很多',
            '能聊聊选择Flask而不是FastAPI的原因吗？',
        ]

        all_users_list = [u for name, u in users.items() if u.status == 1]

        # 为已发布的文章生成评论
        published = [a for a in articles if a.status == 1]
        comment_count = 0

        for article in published:
            # 每篇文章 2-5 条顶级评论
            num_comments = randint(2, 5)
            top_comments = []

            for _ in range(num_comments):
                is_anonymous = random() < 0.25

                if is_anonymous:
                    c = Comment(
                        article=article,
                        nickname=choice(['路人甲', '前端小白', '后端菜鸟', '全栈萌新', '码农老王', '架构师小陈', '数据控', '夜猫子程序员']),
                        email=choice(['luren@qq.com', 'xiaobai@163.com', 'code@foxmail.com', 'dev@gmail.com']),
                        content=choice(comment_pool),
                        status=1,
                    )
                else:
                    c = Comment(
                        article=article,
                        user=choice(all_users_list),
                        content=choice(comment_pool),
                        status=choice([1, 1, 1, 1, 1, 0]),  # 少数待审
                    )

                db.session.add(c)
                db.session.flush()
                top_comments.append(c)
                comment_count += 1

            # 为部分顶级评论添加回复
            for parent in top_comments[:randint(0, 2)]:
                reply = Comment(
                    article=article,
                    user=article.author,
                    content=choice([
                        '谢谢支持！欢迎常来 😊',
                        '好问题，我后续补充到文章里',
                        '感谢指正！已经修改了',
                        '加微信交流：xxx_blog',
                        '代码仓库在 GitHub，文章里有链接',
                        '生产环境跑了半年了，很稳定',
                        '有的，后续会出一个系列',
                    ]),
                    parent=parent,
                    status=1,
                )
                db.session.add(reply)
                comment_count += 1

                # 偶尔有第二层回复
                if random() < 0.3 and parent.user and parent.user != article.author:
                    sub_reply = Comment(
                        article=article,
                        user=parent.user,
                        content='好的好的，感谢回复！',
                        parent=reply,
                        status=1,
                    )
                    db.session.add(sub_reply)
                    comment_count += 1

        db.session.commit()
        print(f'  ✓ {comment_count} 条评论（含回复和嵌套楼中楼）')

        # ============================================
        # 6. 友链
        # ============================================
        print('创建友链...')
        friend_links_data = [
            ('阮一峰的网络日志', 'https://www.ruanyifeng.com/blog/', '科技爱好者周刊，前端技术博客', 1),
            ('酷壳 – CoolShell', 'https://www.coolshell.cn/', '享受编程和技术所带来的快乐', 2),
            ('廖雪峰的官方网站', 'https://www.liaoxuefeng.com/', 'Python / Java / Git 系列教程', 3),
            ('张鑫旭的博客', 'https://www.zhangxinxu.com/', 'CSS / JS / SVG 技术分享', 4),
            ('美团技术团队', 'https://tech.meituan.com/', '美团技术团队的博客', 5),
            ('有赞技术团队', 'https://tech.youzan.com/', '有赞技术团队的实践分享', 6),
            ('字节跳动技术博客', 'https://tech.bytedance.com/', '字节跳动技术团队的博客', 7),
            ('RisingStack Blog', 'https://blog.risingstack.com/', 'Node.js / Microservices / DevOps', 8),
            ('Martin Fowler', 'https://martinfowler.com/', '软件架构、重构、微服务经典文章', 9),
            ('Dan Abramov', 'https://overreacted.io/', 'React 核心开发者的个人博客', 10),
            ('Stack Overflow Blog', 'https://stackoverflow.blog/', 'Stack Overflow 官方博客', 11),
            ('Real Python', 'https://realpython.com/', 'Python 教程和最佳实践', 12),
        ]

        for name, url, desc, order in friend_links_data:
            fl = FriendLink(
                name=name,
                url=url,
                description=desc,
                logo=f'https://api.dicebear.com/8.x/initials/svg?seed={name[:2]}',
                sort_order=order,
                status=1,
            )
            db.session.add(fl)

        # 加一条隐藏的友链（待审核）
        hidden = FriendLink(
            name='待审核的友链',
            url='https://pending.example.com',
            description='这条友链处于隐藏状态，不会在前端展示',
            sort_order=99,
            status=0,
        )
        db.session.add(hidden)

        db.session.commit()
        print(f'  ✓ {len(friend_links_data) + 1} 条友链（含 1 条隐藏）')

        # ============================================
        # 7. 首页轮播图
        # ============================================
        print('创建轮播图...')
        carousel_data = [
            {
                'title':       '欢迎来到我的博客 🎉',
                'image_url':   'https://picsum.photos/seed/blog-banner/900/400',
                'link_url':    '/',
                'description': '分享 Python、前端、DevOps 等技术文章',
                'sort_order':  1,
            },
            {
                'title':       'Flask 项目结构最佳实践',
                'image_url':   'https://picsum.photos/seed/flask-guide/900/400',
                'link_url':    '/articles/1',
                'description': '介绍 Flask 项目的目录结构设计思路和工厂函数模式的好处',
                'sort_order':  2,
            },
            {
                'title':       '打造个人博客的技术选型之路',
                'image_url':   'https://picsum.photos/seed/blog-stack/900/400',
                'link_url':    '/articles/22',
                'description': 'Flask + Vue 3 + MySQL + Docker，一文讲透技术选型',
                'sort_order':  3,
            },
            {
                'title':       'Kubernetes 入门：从 Pod 到 Deployment',
                'image_url':   'https://picsum.photos/seed/k8s-guide/900/400',
                'link_url':    '/articles/10',
                'description': 'K8s 核心概念详解，带你迈出容器编排第一步',
                'sort_order':  4,
            },
            {
                'title':       'Web 常见安全漏洞及防御方案',
                'image_url':   'https://picsum.photos/seed/web-security/900/400',
                'link_url':    '/articles/19',
                'description': 'XSS、CSRF、SQL 注入 —— 每个开发者都应该了解的安全知识',
                'sort_order':  5,
            },
        ]

        for item in carousel_data:
            c = Carousel(
                title=item['title'],
                image_url=item['image_url'],
                link_url=item['link_url'],
                description=item['description'],
                sort_order=item['sort_order'],
                status=1,
            )
            db.session.add(c)

        # 加一条隐藏的轮播图
        hidden_carousel = Carousel(
            title='隐藏的轮播图（测试）',
            image_url='https://picsum.photos/seed/hidden/900/400',
            link_url='/hidden',
            description='这条轮播图处于隐藏状态，不会在前端展示',
            sort_order=99,
            status=0,
        )
        db.session.add(hidden_carousel)

        db.session.commit()
        print(f'  ✓ {len(carousel_data) + 1} 条轮播图（含 1 条隐藏）')

        # ============================================
        # 汇总
        # ============================================
        print('\n' + '=' * 55)
        print('   🎉 假数据初始化完成！')
        print('=' * 55)
        print(f'   用户  : {User.query.count():>4} 条')
        print(f'   分类  : {Category.query.count():>4} 个')
        print(f'   标签  : {Tag.query.count():>4} 个')
        print(f'   文章  : {Article.query.count():>4} 篇  (已发布 {sum(1 for a in articles if a.status==1)}, 草稿 {sum(1 for a in articles if a.status==0)})')
        print(f'   评论  : {Comment.query.count():>4} 条')
        print(f'   友链  : {FriendLink.query.count():>4} 条')
        print(f'   轮播图: {Carousel.query.count():>4} 条')
        print()
        print('   管理员  : admin  / admin123')
        print('   用户    : eugen / 123456')
        print('   用户    : alice / 123456')
        print('   用户    : bob   / 123456')
        print('   用户    : charlie / 123456')
        print('   用户    : diana / 123456')
        print('   用户    : eric  / 123456')
        print('   用户    : fiona / 123456')
        print('=' * 55)


if __name__ == '__main__':
    seed()
