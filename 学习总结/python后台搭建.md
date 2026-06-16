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

## 8、关于JWT  Token 部分

之前是打算将代码按照层进行分级 即 路由层 数据库交互层 工具层 进行分级，后来越进行越感觉不对劲，怎么这代码越写越乱，找了yupiskill 的deep 进行了下分析 发现果然还是过度封装了 导致代码质量提不了多少，但是各种导包，用包越来越频繁，业务逻辑也显得十分混乱了。

现在把代码完全使用一个文件进行 Token的校验，生成，重新签发，删除等操作 方便快速使用。后来又从单 Token 升级成了双 Token（access + refresh），下面按这个新版本来记。

### 从单 Token 到双 Token

之前只签发一个 token，纠结点很矛盾：

- 想安全 → 有效期要短（比如 15 分钟），但用户每 15 分钟就得重新登录，体验差
- 想体验好 → 有效期拉长，可一旦泄露风险就大了

双 Token 就是把一个 token 拆成两个职责分明的：

- **access_token**：短效（15~30 分钟），每个请求带着它鉴权，泄露风险可控
- **refresh_token**：长效（7~30 天），平时不传，只在 access 过期时拿它换新的 access

效果就是 access 过期了用户无感续期，直到 refresh 也过期才需要重新登录。

### 三个关键设计

1. **payload 里带 `type` 字段**（`access` / `refresh`）
   校验时强制校验类型，防止有人拿 refresh 当 access 用（或反过来）。这是双 token 最容易漏的安全点。

2. **Redis 的 key 加前缀**
   `access:{jti}` 和 `refresh:{jti}` 分开存，注销时不会误伤另一类，以后想做「按用户维度踢人下线」也方便。

3. **内部抽公共函数去重**
   access / refresh 的生成、校验、注销逻辑几乎一样，抽成 `_make_token` / `_verify_token` / `_revoke`，对外再暴露 `make_access_token` 这种具体的。既保持单文件，又不重复代码。

```py
# key 前缀 + token 类型常量
ACCESS_PREFIX = 'access:'
REFRESH_PREFIX = 'refresh:'

ACCESS_TYPE = 'access'
REFRESH_TYPE = 'refresh'

# Redis TTL 比 JWT exp 短一点，让"登出 / 吊销"略早生效，留缓冲
_REDIS_TTL_BUFFER = 20
```

### JWT 的生成

内部公共函数（access / refresh 共用）：

```py
# uuid 生成 jti，就是存进 Redis 的键，后面注销 / 查找都靠它
# 时间从 env 取，记得 int() 转一下类型
def _make_token(user, token_type, expire_seconds, key_prefix):
    jti = str(uuid.uuid4())
    now = int(time.time())

    payload = {
        'user_id': user.id,
        'username': user.username,
        'jti': jti,
        'role': user.role,
        'type': token_type,          # 关键：带类型，校验时防 refresh 当 access 用
        'iat': now,
        'exp': now + expire_seconds,
    }

    token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

    # 写入 Redis 白名单，TTL 比 JWT 早 20 秒过期留缓冲
    # 防止 token 实际还没到期、Redis 却先到期导致的业务错误，所以先让 Redis 早一点过期
    redis = get_redis_session()
    key = key_prefix + jti
    redis.set(key, token, ex=expire_seconds - _REDIS_TTL_BUFFER)

    if not redis.get(key):
        raise AppError(code=ApiResponse.TOKEN_IS_NOT_SAVE, message='Token 保存到 Redis 失败')

    return {'jti': jti, 'token': token}
```

对外暴露两个，分别对应短 / 长有效期：

```py
# 短效 access_token
def make_access_token(user):
    return _make_token(
        user, token_type=ACCESS_TYPE,
        expire_seconds=int(Config.JWT_ACCESS_EXPIRES),
        key_prefix=ACCESS_PREFIX,
    )

# 长效 refresh_token
def make_refresh_token(user):
    return _make_token(
        user, token_type=REFRESH_TYPE,
        expire_seconds=int(Config.JWT_REFRESH_EXPIRES),
        key_prefix=REFRESH_PREFIX,
    )
```

> 登录的时候两个一起签发，一起返回给前端。

### JWT 的校验

校验做三件事：解码 JWT → 校验 type 是否匹配 → 查 Redis 白名单还在不在。

```py
def _verify_token(token, expect_type, key_prefix, err_expired, err_invalid):
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AppError(code=err_expired, message='Token 过期了，请重新登录')
    except jwt.InvalidTokenError:
        raise AppError(code=err_invalid, message='Token 无效')

    # 类型必须匹配：refresh 不能当 access 用，反之亦然
    if payload.get('type') != expect_type:
        raise AppError(code=err_invalid, message='Token 类型不正确')

    # Redis 白名单：key 不存在 = 已被吊销 / 登出
    jti = payload.get('jti')
    if not jti or not get_redis_session().get(key_prefix + jti):
        raise AppError(code=ApiResponse.TOKEN_REVOKED, message='Token 已被注销，请重新登录')

    return payload
```

对外两个，各自用对应的错误码（access 过期是 `TOKEN_EXPIRED`，refresh 过期是 `REFRESH_TOKEN_EXPIRED`）：

```py
def verify_access_token(token):
    return _verify_token(
        token, expect_type=ACCESS_TYPE, key_prefix=ACCESS_PREFIX,
        err_expired=ApiResponse.TOKEN_EXPIRED,
        err_invalid=ApiResponse.TOKEN_INVALID,
    )

def verify_refresh_token(token):
    return _verify_token(
        token, expect_type=REFRESH_TYPE, key_prefix=REFRESH_PREFIX,
        err_expired=ApiResponse.REFRESH_TOKEN_EXPIRED,
        err_invalid=ApiResponse.REFRESH_TOKEN_INVALID,
    )
```

### JWT 的注销

注销就是从 Redis 白名单里删掉对应的 key。

```py
def _revoke(key_prefix, jti):
    redis = get_redis_session()
    redis.delete(key_prefix + jti)
    return redis.get(key_prefix + jti) is None

# 对外：两个具体的 + 一个通用的
def revoke_access_token(jti):
    return _revoke(ACCESS_PREFIX, jti)

def revoke_refresh_token(jti):
    return _revoke(REFRESH_PREFIX, jti)

def revoke_token(jti):
    """通用注销（不区分类型，两个前缀都清）：登出时只拿到 jti 就用它"""
    return revoke_access_token(jti) and revoke_refresh_token(jti)
```

### JWT 的刷新（双 Token 的核心）

这是双 token 真正发挥作用的地方：access 过期后，前端拿 refresh_token 来换新的 access。

做法是**轮转**——每次刷新不只发新 access，还顺便发新 refresh、并把旧 refresh 吊销，保证每个 refresh 只能用一次。

```py
def refresh_token(old_refresh_token):
    # 1. 先校验传进来的得是合法的 refresh_token
    payload = verify_refresh_token(old_refresh_token)

    # 2. token 里解码出用户信息，构造简易 user 对象喂给 make_*_token
    class _UserProxy:
        pass

    user = _UserProxy()
    user.id = payload['user_id']
    user.username = payload['username']
    user.role = payload['role']

    # 3. 发新 access + 新 refresh（轮转）
    access = make_access_token(user)
    refresh = make_refresh_token(user)

    # 4. 吊销旧 refresh
    old_jti = payload.get('jti')
    if old_jti:
        revoke_refresh_token(old_jti)

    return {'access': access['token'], 'refresh': refresh['token']}
```

> 防重放：旧 refresh 被吊销后，如果同一个 refresh 又被拿来刷新，`verify_refresh_token` 会因为 Redis 里已经删了而抛 `TOKEN_REVOKED`，从而拦住。以后想做更强（检测到重放就把这个用户的所有会话全部踢下线），在这里扩展就行。

### 路由守卫（装饰器）

请求头里带的是 `Authorization: Bearer <token>`，所以装饰器要先把这个前缀剥掉，再校验，最后把用户信息存到 `g.current_user`，业务层就能直接拿到「当前是谁」。

```py
def _extract_bearer_token():
    """从 Authorization 头解析 'Bearer <token>'，缺失 / 格式错抛 AppError"""
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        raise AppError(code=ApiResponse.LOGIN_REQUIRED, message='请先登录')
    return auth[7:]   # 去掉 'Bearer ' 这 7 个字符

# 普通登录用户
def header_check_token_user(f):
    @wraps(f)
    def check_token(*args, **kwargs):
        token = _extract_bearer_token()
        payload = verify_access_token(token)
        g.current_user = payload   # 业务层用 g.current_user['user_id'] 取当前用户
        return f(*args, **kwargs)
    return check_token

# 管理员（在普通校验基础上，按需补角色判断）
def header_check_token_admin(f):
    @wraps(f)
    def check_token(*args, **kwargs):
        token = _extract_bearer_token()
        payload = verify_access_token(token)
        g.current_user = payload
        # TODO: 在此校验 g.current_user['role'] 是否为管理员角色
        return f(*args, **kwargs)
    return check_token
```

> 第 5 节「路由守卫」一直空着没写，其实就是这两个装饰器的用法——给路由加上 `@header_check_token_user`，就只有登录用户能访问了。

## 9、关于Redis 

他是很简单的一个键值对存储服务器 我对他的使用还不是十分深入，后面还需要深度学习

我在env中使用了他其中的三个库（其实用一个也可以，就是我多少有点代码洁癖）

大体上使用和Mysql逻辑也差不了多少 但是相关的api要简单不少 毕竟就是个键值对服务器嘛~

```py
#注册Redis
import redis


def _make_redis(host, port, password, db, **kwargs):
    """内部工具：根据参数创建 Redis 连接"""
    return redis.Redis(
        host=host,
        port=port,
        password=password,
        db=db,
        decode_responses=True,
        socket_connect_timeout=5,
        **kwargs,
    )


# ---- 三个 Redis 连接，懒加载 ----

_redis_session = None
_redis_cache = None
_redis_ratelimit = None


def get_redis_session():
    """获取 session Redis 连接（懒加载）"""
    global _redis_session
    if _redis_session is None:
        _redis_session = _make_redis(
            Config.REDIS_HOST, Config.REDIS_PORT,
            Config.REDIS_PASSWORD, int(Config.REDIS_DB_SESSION),
        )
    return _redis_session


def get_redis_cache():
    """获取 cache Redis 连接（懒加载）"""
    global _redis_cache
    if _redis_cache is None:
        _redis_cache = _make_redis(
            Config.REDIS_HOST, Config.REDIS_PORT,
            Config.REDIS_PASSWORD, int(Config.REDIS_DB_CACHE),
        )
    return _redis_cache


def get_redis_ratelimit():
    """获取限流 Redis 连接（懒加载）"""
    global _redis_ratelimit
    if _redis_ratelimit is None:
        _redis_ratelimit = _make_redis(
            Config.REDIS_HOST, Config.REDIS_PORT,
            Config.REDIS_PASSWORD, int(Config.REDIS_DB_RATELIMIT),
        )
    return _redis_ratelimit


def init_redis(app=None):
    """应用启动时预初始化所有 Redis 连接，提前发现连接问题"""
    try:
        get_redis_session().ping()
        get_redis_cache().ping()
        get_redis_ratelimit().ping()
    except redis.ConnectionError as e:
        raise RuntimeError(f'Redis 连不上，检查地址和密码: {e}')


```






```py
# 存入
redis().set(jti,'token',ex=1800) (键，值，过期时间)

# 查找
redis().get(jti)  #有就返回具体键值对，无就返回None

#删除
redis().delete(jti) 
```




