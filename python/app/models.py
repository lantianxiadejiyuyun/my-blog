from datetime import datetime

import bcrypt

from app.extensions import db

# ============================================================
# 文章-标签 多对多关联表
# ============================================================

article_tags = db.Table('article_tags',
    db.Column('article_id', db.Integer, db.ForeignKey('articles.id'), primary_key=True),  # 文章ID
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),           # 标签ID
)

# ============================================================
# User 用户表
# ============================================================

class User(db.Model):
    __tablename__ = 'user'

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 自增主键
    username    = db.Column(db.String(50), unique=True, nullable=False)        # 用户名，唯一，不能为空
    password    = db.Column(db.String(200), nullable=False)                    # bcrypt 加密后的密码
    email       = db.Column(db.String(100))                                   # 邮箱
    avatar      = db.Column(db.String(500))                                   # 头像URL
    bio         = db.Column(db.String(500))                                   # 个人简介
    role        = db.Column(db.String(20), default='user')                    # 角色：serveradmin / admin / user
    status      = db.Column(db.SmallInteger, default=1)                       # 1=正常 0=禁用
    check_number = db.Column(db.SmallInteger, default=0)                      # 连续登录失败次数
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)             # 创建时间
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间

    articles = db.relationship('Article', backref='author', lazy='dynamic')   # 用户写的文章
    comments = db.relationship('Comment', backref='user', lazy='dynamic')     # 用户发表的评论


# ============================================================
# Article 文章表
# ============================================================

class Article(db.Model):
    __tablename__ = 'articles'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 自增主键
    title       = db.Column(db.String(200), nullable=False)                    # 标题
    content     = db.Column(db.Text)                                           # 正文（Markdown）
    summary     = db.Column(db.String(500))                                    # 摘要
    cover       = db.Column(db.String(500))                                    # 封面图URL
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))        # 所属分类
    author_id   = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 作者
    status      = db.Column(db.SmallInteger, default=0)                        # 0=草稿 1=已发布
    view_count  = db.Column(db.Integer, default=0)                             # 浏览量
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)              # 创建时间
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间

    tags     = db.relationship('Tag', secondary=article_tags, backref='articles')  # 多对多标签
    comments = db.relationship('Comment', backref='article', lazy='dynamic')       # 文章下的评论


# ============================================================
# Category 分类表
# ============================================================

class Category(db.Model):
    __tablename__ = 'categories'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 自增主键
    name        = db.Column(db.String(50), unique=True, nullable=False)        # 分类名，唯一
    description = db.Column(db.String(200))                                    # 分类描述

    articles = db.relationship('Article', backref='category', lazy='dynamic')  # 该分类下的文章


# ============================================================
# Tag 标签表
# ============================================================

class Tag(db.Model):
    __tablename__ = 'tags'

    id   = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 自增主键
    name = db.Column(db.String(50), unique=True, nullable=False)        # 标签名，唯一


# ============================================================
# Comment 评论表
# ============================================================

class Comment(db.Model):
    __tablename__ = 'comments'

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)   # 自增主键
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)  # 所属文章
    user_id    = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # 登录用户（空=游客）
    nickname   = db.Column(db.String(50))                                      # 游客昵称
    email      = db.Column(db.String(100))                                     # 邮箱
    content    = db.Column(db.Text, nullable=False)                            # 评论内容
    parent_id  = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)  # 回复的评论ID（空=顶级评论）
    status     = db.Column(db.SmallInteger, default=0)                         # 0=待审 1=通过 2=拒绝
    created_at = db.Column(db.DateTime, default=datetime.utcnow)               # 创建时间

    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')  # 子回复


# ============================================================
# FriendLink 友链表
# ============================================================

class FriendLink(db.Model):
    __tablename__ = 'friend_links'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 自增主键
    name        = db.Column(db.String(100), nullable=False)                    # 网站名称
    url         = db.Column(db.String(500), nullable=False)                    # 链接地址
    description = db.Column(db.String(300))                                    # 站点描述
    logo        = db.Column(db.String(500))                                    # logo/头像 URL
    sort_order  = db.Column(db.Integer, default=0)                             # 排序（越小越靠前）
    status      = db.Column(db.SmallInteger, default=1)                        # 1=显示 0=隐藏
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)              # 创建时间


# ============================================================
# Carousel 首页轮播图表
# ============================================================

class Carousel(db.Model):
    __tablename__ = 'carousels'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 自增主键
    title       = db.Column(db.String(100), nullable=False)                    # 轮播图标题
    image_url   = db.Column(db.String(500), nullable=False)                    # 图片URL
    link_url    = db.Column(db.String(500))                                    # 点击跳转链接
    description = db.Column(db.String(300))                                    # 描述文字
    sort_order  = db.Column(db.Integer, default=0)                             # 排序（越小越靠前）
    status      = db.Column(db.SmallInteger, default=1)                        # 1=显示 0=隐藏
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)              # 创建时间
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间
