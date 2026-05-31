from app import db
from datetime import datetime

# User 表
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100))
    avatar = db.Column(db.String(500))
    bio = db.Column(db.String(500))
    role = db.Column(db.String(20), default='user')
    status = db.Column(db.SmallInteger, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # id          # 自增主键，唯一标识每个用户，1 2 3 自动往下排
    # username    # 用户名，最长50字符，不能重复不能为空，登录用
    # password    # bcrypt加密后的密码串，最长200字符，不能为空
    # email       # 邮箱，可选
    # avatar      # 头像url，存的是图片链接地址，最长500字符
    # bio         # 个人简介/签名，最长500字符
    # role        # 角色：serveradmin / admin / user，默认新注册是user
    # status      # 2=禁言（约等于） 1=正常 0=禁用 ，存小整数省空间
    # created_at  # 创建时间，插入行时自动填当前时间
    # updated_at  # 更新时间，每次修改行自动更新为当前时间

