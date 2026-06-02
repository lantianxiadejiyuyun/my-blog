# Python 后台搭建的总结

## 1、关于环境变量 .env 文件 

环境变量加载，强制覆盖已有环境变量

```py
from dotenv import load_dotenv

load_dotenv(override=True)  # 强制覆盖已有环境变量


# 读取环境变量
xxx = os.environ.get('xxx', '')
```

## 2、env 环境检查

为了方便用户快速检查环境变量是否正确配置，我添加了utils.py 这个文件 用来校验是否有输入正确的环境变量配置参数

```py
# 配置检查单 utils.py

import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_start():
    required = [
        ('DB_HOST', os.environ.get('DB_HOST')),
        ('DB_PORT', os.environ.get('DB_PORT')),
        ('DB_USER', os.environ.get('DB_USER')),
        ('DB_PASSWORD', os.environ.get('DB_PASSWORD')),
        ('DB_NAME', os.environ.get('DB_NAME')),
        ('REDIS_HOST', os.environ.get('REDIS_HOST')),
        ('REDIS_PORT', os.environ.get('REDIS_PORT')),
        ('REDIS_PASSWORD', os.environ.get('REDIS_PASSWORD')),
        ('REDIS_DB', os.environ.get('REDIS_DB')),
        ('JWT_SECRET_KEY', os.environ.get('JWT_SECRET_KEY')),
        ('JWT_ACCESS_EXPIRES', os.environ.get('JWT_ACCESS_EXPIRES')),
        ('FLASK_ENV', os.environ.get('FLASK_ENV')),
        ('FLASK_PORT', os.environ.get('FLASK_PORT')),
        ('FLASK_DEBUG', os.environ.get('FLASK_DEBUG')),
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

from utils import check_start, logger as env_logger

# 检查环境变量
if not check_start():
    env_logger.error('缺少必填环境变量，无法启动')
    # 强制退出进程 
    sys.exit(1)
```

## 3、初始化 项目

 在config.py 中  导入对应的env环境变量，拼接连接串 封装成类 方便快速调用

```py
import os

class Config:
    # MySQL
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
    DB_USER = os.environ.get('DB_USER')
    DB_NAME = os.environ.get('DB_NAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')

    # SQLAlchemy 连接
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}"
        f"@{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}"
        f"?charset=utf8mb4"
    )

    # Redis
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
# app/__init__.py — 应用工厂
from flask_cors import CORS
from flask import Flask

from .public import blueprints as public_bps
from .config import Config
from .extensions import db


API_PREFIX = '/api'

def register_blueprints(app):
    for bp, prefix in public_bps:
        app.register_blueprint(bp, url_prefix=f'{API_PREFIX}/{prefix}')


def create_app():
    app = Flask(__name__)
    # 把 Config 类里的所有大写变量自动加载到 Flask 的 app.config 里
    app.config.from_object(Config)

    # 把数据库对象绑定到 app
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
# main.py
import sys
import os

from dotenv import load_dotenv
load_dotenv(override=True)  # 最早加载，防止出现读空值

from app import create_app
from utils import check_start, logger as env_logger

# 检查环境变量，检查完毕后启动 Flask
if not check_start():
    env_logger.error('缺少必填环境变量，无法启动')
    sys.exit(1)

# Flask 配置
class FlaskConfig:
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 'yes')
    FLASK_PORT = os.environ.get('FLASK_PORT', 5000)

# 启动
app = create_app()

# 使用动态配置 port 和 debug
if __name__ == '__main__':
    app.run(debug=FlaskConfig.FLASK_DEBUG, port=int(FlaskConfig.FLASK_PORT))
```

## 4、路由的统一封装

这个项目使用两层结构

```python
第一层 app/ __init__.py 
	
	第二层 public / __init__.py 将对应文件夹下的路由统一记录
    			 /	blog.py
        		 /	health.py
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

## 6、关于上面的代码会导致循环导入问题

修改之前的启动链子

```py
main.py
	—> from app import creat_app # 开始加载 app/__init__.py
    	-> from.public 			 # 加载public/ init.py
        	-> from .blog 		 # 加载blog.py 其中会需要导入 db  但是db 此时还有没有初始化
            	-> from app import db #  此处报错
```

Deep对这个错误如下表述

根因就是一句话：blog.py 找 db 的时候，db = SQLAlchemy() 这行代码还没被执行到。

解法也简单：把 db 从链条的末端（__init__.py）移到链条的最前端（extensions.py），让它成为第一个准备好了的东西。

## 7、关于错误处理

我学习了其他框架的报错逻辑设计了这个三层报错提示

AppError 只是个入口 调用之后 Flask 会调用三层代码 进行错误处理

```py
# 第一部分 开发者自定义部分 用于处理具体业务报错 比如参数不对、类型错误、业务错误等 
# 第二部分 Flask 框架抛出部分 HTTP 层错误
# 第三部分 兜底 用于处理未知错误，并且加入服务器日志
```

示例代码

```py
__init__.py
# Flask项目入口
from flask_cors import CORS
from flask import Flask

from .public import blueprints as public_bps
from .config import Config
from .extensions import db
from .errors import register_error_handlers #导入一下


API_PREFIX = '/api'

def register_blueprints(app):
    for bp,prefix in public_bps:
        app.register_blueprint(bp,url_prefix=f'{API_PREFIX}/{prefix}')


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    register_blueprints(app)
    register_error_handlers(app)	# 把错误处理注册到应用工厂中
    CORS(app)

    return app
```



```py
# 在 Flask 框架中修改对应的报错参数，接收从开发者传入的自定义参数
class AppError(Exception):
    """在业务代码里主动抛出，带上业务码和中文提示"""
    def __init__(self, code, message, http_code=400):
        self.code = code
        self.message = message
        self.http_code = http_code
        
# 用法 
raise AppError(code, message, http_code=400)
```

三层错误处理

```py
from werkzeug.exceptions import HTTPException
from .response import fail


def register_error_handlers(app):
    """三层错误捕获，按 AppError → HTTPException → Exception 优先级递减匹配"""

    # 第1层：你主动抛出的业务异常
    @app.errorhandler(AppError)
    def handle_app_error(e):
        return fail(e.code, e.message, http_status=e.http_code)

    # 第2层：Flask/Werkzeug 自己的 HTTP 异常（404、405、500 等）
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return fail(e.code or 500, e.description, http_status=e.code or 500)

    # 第3层：兜底，所有没被上面两层接住的未知异常
    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        app.logger.exception('未捕获的异常')  # 这个记日志很重要，不然线上炸了都不知道
        return fail(500, '服务器内部错误，请稍后重试', http_status=500)
```
