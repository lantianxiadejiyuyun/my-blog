# Python 后台搭建的总结

## 1、关于环境变量 .env 文件 

环境变量加载，强制覆盖

```py
from dotenv import load_dotenv

load_dotenv(verbose=True) # 强制覆盖环境


# 默认导入
xxx = os.environ.get('xxx','')
```

## 2、env 环境检查

为了方便用户快速检查环境变量是否正确配置，我添加了utils.py 这个文件 用来校验是否有输入正确的环境变量配置参数

```py
# 配置检查单 utils.py

import os
import logging

logger = logging.getLogger(__name__)

def checkStart():
    required = [
        ('DB_HOST', os.getenv('DB_HOST')),
        ('DB_PORT', os.getenv('DB_PORT')),
        ('DB_USER', os.getenv('DB_USER')),
        ('DB_PASSWORD', os.getenv('DB_PASSWORD')),
        ('DB_NAME', os.getenv('DB_NAME')),
        ('REDIS_HOST', os.getenv('REDIS_HOST')),
        ('REDIS_PORT', os.getenv('REDIS_PORT')),
        ('REDIS_PASSWORD', os.getenv('REDIS_PASSWORD')),
        ('REDIS_DB', os.getenv('REDIS_DB')),
        ('JWT_SECRET_KEY', os.getenv('JWT_SECRET_KEY')),
        ('JWT_ACCESS_EXPIRES', os.getenv('JWT_ACCESS_EXPIRES')),
        ('FLASK_ENV', os.getenv('FLASK_ENV')),
        ('FLASK_PORT', os.getenv('FLASK_PORT')),
        ('FLASK_DEBUG', os.getenv('FLASK_DEBUG')),
    ]

    missing = [name for name, value in required if not value]

    if missing:
        logger.error('缺少必填环境变量: %s', ', '.join(missing))
        return False

    return True


```

**关于如何使用**

```py
# 关于如何使用
import sys

from utils import checkStart, logger as env_logger

# 检查环境变量
if not checkStart():
    env_logger.error('缺少必填环境变量，无法启动')
    # 强制退出进程 
    sys.exit(1)
```

## 3、初始化 项目

 在config.py 中  导入对应的env环境变量，拼接连接串 封装成类 方便快速调用

```py
import os

class Config :
    # Mysql
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
    DB_USER = os.environ.get('DB_USER')
    DB_NAME = os.environ.get('DB_NAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')

    # SQLAlchemy 链接 关键配置链接
    SQLALCHEMY_DATABASE_URI =  f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}" f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}" f"?charset=utf8mb4"

    # Reids
    REDIS_HOST = os.environ.get('REDIS_HOST')
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
    REDIS_PORT = os.environ.get('REDIS_PORT')
    REDIS_DB = os.environ.get('REDIS_DB')

    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_EXPIRES = os.environ.get('JWT_ACCESS_EXPIRES')
```

app下 

```py
# 统一注册
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from .public import blueprints as public_bps
from .config import Config


API_PREFIX = '/api'

def register_blueprints(app):
    for bp,prefix in public_bps:
        app.register_blueprint(bp,url_prefix=f'{API_PREFIX}/{prefix}')


# 项目初始化 将关键的代码 进行封装
# 初始化数据库对象
db = SQLAlchemy()
def create_app():
    # 创建Flask app 
    app = Flask(__name__)
    # 把 Config 类里的所有大写变量自动加载到 Flask 的 app.config 里。
    app.config.from_object(Config)

    # 把数据库对象 进行绑定 
    db.init_app(app)
    
    # 注册路由
    register_blueprints(app)
    # 跨域处理
    CORS(app)

    return app
```

​    **app.config.from_object(Config)** 

好处：db.init_app(app) 的时候，SQLAlchemy 会自动从 app.config 里找 SQLALCHEMY_DATABASE_URI 这个 key 来连接数据库。你不需要手动把配置传给 db。

Flask 和它的扩展之间的约定就是：扩展去 app.config 里按约定好的 key 读配置，from_object() 只是批量塞进去的方式。

```py
main.py
# 导入已经封装好的app 
from dotenv import load_dotenv
load_dotenv(verbose=True) # 最早加载 防止出现读空值

from app import create_app
from utils import checkStart, logger as env_logger

# 检查环境变量 检查完毕后启动flask
if not checkStart():
    env_logger.error('缺少必填环境变量，无法启动')
    sys.exit(1)

# Flask 配置
class FlaskConfig :
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', False)
    FLASK_PORT = os.environ.get('FLASK_PORT', 5000)

# 启动
app = create_app()

# 使用动态配置porst 和 debug 
if __name__ == '__main__':
    app.run(debug= FlaskConfig.FLASK_DEBUG,port=int (FlaskConfig.FLASK_PORT));
```

## 4、路由的统一封装

这个项目使用两层结构

```python
第一层 app/ __init__.py 
	
	第二层 public / __init__.py 将对应文件夹下的路由统一记录
    			 /	blog.py
        		 /	healt.py
        		 /	login.py
        		 /	......
    第二层 admin  / __init__.py 将对应文件夹下的路由统一记录
    			 /	xxx.py
        		 /	xxx.py
        		 /	xxx.py
        		 /	....
    第二层 user   / __init__.py 将对应文件夹下的路由统一记录
    			 /	xxx.py
        		 /	xxx.py
        		 /	xxx.py
        		 /	....
```

**如何导入 和 使用**

第一层

```py
from .public import blueprints as public_bps # as重命名了一下

API_PREFIX = '/api'

def register_blueprints(app):
    for bp,prefix in public_bps + admin_bps + user_bps: # 循环遍历出其中的 对象和对url 进行拼接
        app.register_blueprint(bp,url_prefix=f'{API_PREFIX}/{prefix}')
```

第二层

```py
from .login import login
from .health import health
from .blog import blog

blueprints = [
    # 对象 / 对应的地址
    (health, '/health'),
    (login, '/login'),
    (blog, '/blog'),
]
```

文件内部长这样

```
from flask import Blueprint, jsonify


login = Blueprint('login', __name__)

@login.route('/')
def index():
    return jsonify('hello world')
```

## 5、关于路由守卫  （过会写）
