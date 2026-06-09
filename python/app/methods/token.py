from functools import wraps

import time
import uuid

import jwt
from flask import g, request

from app.config import Config
from app.extensions import get_redis_session
from app.utils.errors import AppError
from app.utils.response import ApiResponse, fail

def make_token(user):
    """生成 JWT + 写入 Redis，返回 {jti, token}"""
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


def verify_token(token):
    """验证 JWT：成功返回 payload，过期/无效/被吊销 抛 AppError"""
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


def revoke_token(jti):
    """注销 token：从 Redis 删除 返回 True/False"""
    redis = get_redis_session()
    redis.delete(jti)
    return redis.get(jti) is None

#  更新token
def refresh_token(old_token):
    """用旧 token 换新 token：验证通过后发新token 吊销旧token"""
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


# ============================================================
# 装饰器
# ============================================================

def login_required(f):
    """登录校验装饰器：从 Authorization header 取 token，验证通过后把 payload 写入 g.current_user

    用法:
        @app.route('/api/user/profile')
        @login_required
        def profile():
            user_id = g.current_user['user_id']
            ...
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # 取 header
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return fail(code=ApiResponse.LOGIN_REQUIRED, message='请先登录')

        token = auth_header[7:]  # 去掉 "Bearer " 前缀

        # 验证 token（过期/无效/吊销 会抛 AppError，被全局异常处理器接住）
        payload = verify_token(token)

        # 注入到 g，路由函数直接取
        g.current_user = payload

        return f(*args, **kwargs)

    return decorated


def role_required(*roles):
    """角色校验装饰器：在 login_required 基础上检查角色

    用法:
        @app.route('/api/admin/users')
        @role_required('admin', 'serveradmin')
        def manage_users():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # 先做登录校验
            auth_header = request.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                return fail(code=ApiResponse.LOGIN_REQUIRED, message='请先登录')

            token = auth_header[7:]
            payload = verify_token(token)
            g.current_user = payload

            # 再检查角色
            if payload.get('role') not in roles:
                return fail(code=ApiResponse.NO_PERMISSION, message='权限不足')

            return f(*args, **kwargs)

        return decorated
    return decorator
