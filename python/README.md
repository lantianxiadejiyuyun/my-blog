# My Blog — Flask API 服务器

Flask 纯 API 后端，为 Vue 前端提供数据接口。

## 技术栈

| 组件 | 选型 |
|------|------|
| Web 框架 | Flask 3.x |
| 数据库 | MySQL 8.0 + SQLAlchemy ORM |
| 缓存 / Token 存储 | Redis 7.x |
| 认证 | JWT (PyJWT) + bcrypt |
| 跨域 | Flask-CORS |

## 快速启动

```bash
# 1. 进入目录
cd python

# 2. 创建虚拟环境
python -m venv .venv

# 3. 激活虚拟环境 (Windows)
.venv\Scripts\activate

# 4. 安装依赖
pip install -r requirements.txt

# 5. 复制环境变量配置，修改数据库和 Redis 连接信息
cp .env.example .env

# 6. 初始化数据库（建表 + 创建初始 serveradmin 账号）
python init_db.py

# 7. 启动
python main.py
# → 默认监听 http://localhost:5000
```

## 环境变量 (.env)

```env
# 数据库
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=my_blog

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0

# JWT
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ACCESS_EXPIRES=1800

# App
FLASK_ENV=development
```

## 目录结构

```
python/
├── app/
│   ├── __init__.py      # create_app() 工厂函数
│   ├── config.py        # 配置类
│   ├── models.py        # 数据库模型
│   ├── middleware.py    # JWT + 权限装饰器
│   ├── utils.py         # 统一响应
│   ├── auth.py          # 认证 API
│   ├── articles.py      # 文章 API
│   ├── categories.py    # 分类 API
│   ├── tags.py          # 标签 API
│   ├── comments.py      # 评论 API
│   └── users.py         # 用户管理 API
├── init_db.py           # 建表 + 初始账号
├── requirements.txt
├── main.py              # 入口
└── README.md
```

---

## 三级权限系统

### 角色层级

```
serveradmin（超级管理员）
  └─ admin（管理员）
      └─ user（普通用户）
```

### 权限矩阵

| 操作 | user | admin | serveradmin |
|------|:----:|:-----:|:-----------:|
| 浏览文章/评论 | ✓ | ✓ | ✓ |
| 发表评论 | ✓ | ✓ | ✓ |
| 删除自己的评论 | ✓ | ✓ | ✓ |
| 编辑自己的信息 | ✓ | ✓ | ✓ |
| 写文章 | ✗ | ✓ | ✓ |
| 管理分类/标签 | ✗ | ✓ | ✓ |
| 审核/删除任意评论 | ✗ | ✓ | ✓ |
| 管理用户/改角色 | ✗ | ✗ | ✓ |

### 实现方式

两个装饰器完成所有权限控制：

```python
@app.route('/api/articles', methods=['POST'])
@login_required
@require_role('admin', 'serveradmin')
def create_article():
    ...
```

---

## Token 认证流程

```mermaid
登录请求 → 验证账号密码
         → 生成 access_token (JWT, 30min)
         → 生成 refresh_token (UUID, 7天)
         → 两个 token 都存 Redis
         → 返回给客户端

后续请求 → Header: Authorization: Bearer <access_token>
        → @login_required 验证 JWT → 查 Redis 确认有效 → 注入 g.current_user
        → @require_role 检查角色权限

access_token 到期 → POST /api/auth/refresh 用 refresh_token 换新

登出 → 从 Redis 删除两个 token
```

---

## 数据库表设计

### users
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK | 自增 |
| username | VARCHAR(50) UNIQUE | 用户名 |
| password | VARCHAR(200) | bcrypt 密文 |
| email | VARCHAR(100) | 邮箱 |
| avatar | VARCHAR(500) | 头像 URL |
| bio | VARCHAR(500) | 个人简介 |
| role | ENUM | serveradmin / admin / user |
| status | TINYINT | 1=正常 0=禁用 |
| created_at | DATETIME | |
| updated_at | DATETIME | |

### articles
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK | 自增 |
| title | VARCHAR(200) | 标题 |
| content | LONGTEXT | 正文 Markdown |
| summary | VARCHAR(500) | 摘要 |
| cover | VARCHAR(500) | 封面图 URL |
| category_id | INT FK | 关联分类 |
| author_id | INT FK | 关联用户 |
| status | TINYINT | 0=草稿 1=已发布 |
| view_count | INT | 浏览量 |
| created_at | DATETIME | |
| updated_at | DATETIME | |

### categories
| 字段 | 类型 |
|------|------|
| id | INT PK |
| name | VARCHAR(50) UNIQUE |
| description | VARCHAR(200) |

### tags
| 字段 | 类型 |
|------|------|
| id | INT PK |
| name | VARCHAR(50) UNIQUE |

### article_tags
| 字段 | 类型 |
|------|------|
| article_id | INT FK (PK) |
| tag_id | INT FK (PK) |

### comments
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK | |
| article_id | INT FK | 所属文章 |
| user_id | INT FK nullable | 登录用户 |
| nickname | VARCHAR(50) | 昵称（非登录用户） |
| email | VARCHAR(100) | 邮箱 |
| content | TEXT | 评论内容 |
| parent_id | INT nullable | 回复的评论 id |
| status | TINYINT | 0=待审 1=通过 2=拒绝 |
| created_at | DATETIME | |

---

## API 接口文档

> 统一响应格式：`{ "code": 200, "message": "ok", "data": {} }`

### 认证 auth（全部公开）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/auth/login | 登录，返回 access_token / refresh_token |
| POST | /api/auth/register | 注册，默认 user 角色 |
| POST | /api/auth/refresh | 用 refresh_token 换新的 access_token |
| POST | /api/auth/logout | 登出，销毁 token |

**POST /api/auth/login**
```json
// 请求
{ "username": "admin", "password": "123456" }
// 响应
{ "code": 200, "message": "ok", "data": {
    "access_token": "eyJ...",
    "refresh_token": "a1b2c3...",
    "user": { "id": 1, "username": "admin", "role": "serveradmin" }
}}
```

### 文章 articles

| 方法 | 路径 | 权限 | 说明 |
|------|------|------|------|
| GET | /api/articles | 公开 | 列表，支持 ?page=&size=&category=&tag=&status=&keyword= |
| GET | /api/articles/:id | 公开 | 详情 |
| POST | /api/articles | admin+ | 创建 |
| PUT | /api/articles/:id | admin+ | 编辑 |
| DELETE | /api/articles/:id | admin+ | 删除 |

### 分类 categories

| 方法 | 路径 | 权限 |
|------|------|------|
| GET | /api/categories | 公开 |
| POST | /api/categories | admin+ |
| PUT | /api/categories/:id | admin+ |
| DELETE | /api/categories/:id | admin+ |

### 标签 tags

| 方法 | 路径 | 权限 |
|------|------|------|
| GET | /api/tags | 公开 |
| POST | /api/tags | admin+ |
| PUT | /api/tags/:id | admin+ |
| DELETE | /api/tags/:id | admin+ |

### 评论 comments

| 方法 | 路径 | 权限 |
|------|------|------|
| GET | /api/articles/:id/comments | 公开 |
| POST | /api/articles/:id/comments | user+ |
| DELETE | /api/comments/:id | 本人或 admin+ |
| PUT | /api/comments/:id/status | admin+ |

### 用户管理 users

| 方法 | 路径 | 权限 |
|------|------|------|
| GET | /api/users | serveradmin |
| PUT | /api/users/:id/role | serveradmin |
| PUT | /api/users/:id/status | serveradmin |
| GET | /api/users/me | user+ |
| PUT | /api/users/me | user+ |

---

## 依赖清单 (requirements.txt)

```
flask==3.1.*
flask-sqlalchemy==3.1.*
flask-cors==5.0.*
pymysql==1.1.*
redis==5.*
pyjwt==2.10.*
bcrypt==4.*
python-dotenv==1.*
```
