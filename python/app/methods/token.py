import time
import uuid
import jwt

from functools import wraps
from flask import request, g, jsonify

from app.config import Config
from app.extensions import get_redis_session
from app.utils.errors import AppError
from app.utils.response import ApiResponse

### 生成 JWT + 写入 Redis，返回 {jti, token}"""
def make_token(user):
    jti = str(uuid.uuid4())
    now = int(time.time())
    expire_seconds = int(Config.JWT_ACCESS_EXPIRES)

    payload = {
        'user_id': user.id,
        'username': user.username,
        'jti': jti,
        'role': user.role,
        'iat': now,
        'exp': now + expire_seconds,
    }

    token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

    # 写入 Redis，过期比 JWT 早 20 秒留缓冲
    redis = get_redis_session()
    redis.set(jti, token, ex=expire_seconds - 20)

    # 验证写入成功
    if not redis.get(jti):
        raise AppError(code=ApiResponse.TOKEN_IS_NOT_SAVE, message='Token 保存到 Redis 失败')

    return {'jti': jti, 'token': token}


### 验证 JWT：成功返回 payload，过期/无效/被吊销 抛 AppError
def verify_token(token):
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AppError(code=ApiResponse.TOKEN_EXPIRED, message='Token 过期了，请重新登录')
    except jwt.InvalidTokenError:
        raise AppError(code=ApiResponse.TOKEN_INVALID, message='Token 无效')

    # 检查是否已被服务端吊销（Redis 中是否还存在）
    jti = payload.get('jti')
    if jti and not get_redis_session().get(jti):
        raise AppError(code=ApiResponse.TOKEN_REVOKED, message='Token 已被注销，请重新登录')

    return payload


### 注销 token：从 Redis 删除 返回 True/False
def revoke_token(jti):
    redis = get_redis_session()
    redis.delete(jti)
    return redis.get(jti) is None

#  用旧 token 换新 token：验证通过后发新token 吊销旧token
def refresh_token(old_token):
    payload = verify_token(old_token)

    # 构造一个简易 user 对象给 make_token
    class _UserProxy:
        pass

    user = _UserProxy()
    user.id = payload['user_id']
    user.username = payload['username']
    user.role = payload['role']

    # 发新 token
    result = make_token(user)

    # 吊销旧 token
    old_jti = payload.get('jti')
    if old_jti:
        revoke_token(old_jti)

    return result

### token 装饰器 普通权限
def header_check_token_user(f):
    @wraps(f)
    def check_token(*args, **kwargs):
        auth = request.headers.get('Authorization', '')

        # 校验token
        verify_token(auth)

        return f(*args, **kwargs)

    return check_token


def header_check_token_admin(f):
    @wraps(f)
    def check_token(*args, **kwargs):
        auth = request.headers.get('Authorization', '')

        # 校验token
        verify_token(auth)

        return f(*args, **kwargs)

    return check_token
