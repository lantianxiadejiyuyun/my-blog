import time
import uuid
import jwt

from functools import wraps
from flask import request, g

from app.config import Config
from app.extensions import get_redis_session
from app.utils.errors import AppError
from app.utils.response import ApiResponse

# ============ 常量：Redis key 前缀 + token 类型 ============
ACCESS_PREFIX = 'access:'
REFRESH_PREFIX = 'refresh:'

ACCESS_TYPE = 'access'
REFRESH_TYPE = 'refresh'

# Redis TTL 比 JWT exp 短一点，让"登出 / 吊销"略早生效，留缓冲
_REDIS_TTL_BUFFER = 20


# ============================================================
# 内部公共工具
# ============================================================

def _make_token(user, token_type, expire_seconds, key_prefix):
    """构建 JWT + 写入 Redis 白名单。返回 {'jti': jti, 'token': token}"""
    jti = str(uuid.uuid4())
    now = int(time.time())

    payload = {
        'user_id': user.id,
        'username': user.username,
        'jti': jti,
        'role': user.role,
        'type': token_type,          # 关键：带上类型，校验时防 refresh 当 access 用（反之亦然）
        'iat': now,
        'exp': now + expire_seconds,
    }

    token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

    redis = get_redis_session()
    key = key_prefix + jti
    redis.set(key, token, ex=expire_seconds - _REDIS_TTL_BUFFER)

    if not redis.get(key):
        raise AppError(code=ApiResponse.TOKEN_IS_NOT_SAVE, message='Token 保存到 Redis 失败')

    return {'jti': jti, 'token': token}


def _verify_token(token, expect_type, key_prefix, err_expired, err_invalid):
    """解码 JWT + 校验类型 + 校验 Redis 白名单。成功返回 payload，失败抛 AppError"""
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AppError(code=err_expired, message='Token 过期了，请重新登录')
    except jwt.InvalidTokenError:
        raise AppError(code=err_invalid, message='Token 无效')

    # 类型必须匹配：refresh 不能当 access 用，access 也不能当 refresh 用
    if payload.get('type') != expect_type:
        raise AppError(code=err_invalid, message='Token 类型不正确')

    # Redis 白名单：key 不存在 = 已被吊销 / 登出
    jti = payload.get('jti')
    if not jti or not get_redis_session().get(key_prefix + jti):
        raise AppError(code=ApiResponse.TOKEN_REVOKED, message='Token 已被注销，请重新登录')

    return payload


def _revoke(key_prefix, jti):
    """删除指定前缀下的 jti，返回是否删除成功"""
    redis = get_redis_session()
    redis.delete(key_prefix + jti)
    return redis.get(key_prefix + jti) is None


# ============================================================
# 构建（2 个）
# ============================================================

### 构建短效 access_token：写入 Redis，返回 {jti, token}
def make_access_token(user):
    return _make_token(
        user,
        token_type=ACCESS_TYPE,
        expire_seconds=int(Config.JWT_ACCESS_EXPIRES),
        key_prefix=ACCESS_PREFIX,
    )


### 构建长效 refresh_token：写入 Redis，返回 {jti, token}
def make_refresh_token(user):
    return _make_token(
        user,
        token_type=REFRESH_TYPE,
        expire_seconds=int(Config.JWT_REFRESH_EXPIRES),
        key_prefix=REFRESH_PREFIX,
    )


# ============================================================
# 校验（2 个）
# ============================================================

### 校验 access_token：成功返回 payload，过期 / 无效 / 吊销 抛 AppError
def verify_access_token(token):
    return _verify_token(
        token,
        expect_type=ACCESS_TYPE,
        key_prefix=ACCESS_PREFIX,
        err_expired=ApiResponse.TOKEN_EXPIRED,
        err_invalid=ApiResponse.TOKEN_INVALID,
    )


### 校验 refresh_token：成功返回 payload，过期 / 无效 / 吊销 抛 AppError
def verify_refresh_token(token):
    return _verify_token(
        token,
        expect_type=REFRESH_TYPE,
        key_prefix=REFRESH_PREFIX,
        err_expired=ApiResponse.REFRESH_TOKEN_EXPIRED,
        err_invalid=ApiResponse.REFRESH_TOKEN_INVALID,
    )


# ============================================================
# 注销（2 个 + 1 个通用兼容）
# ============================================================

### 注销 access_token：从 Redis 删除，返回 True/False
def revoke_access_token(jti):
    return _revoke(ACCESS_PREFIX, jti)


### 注销 refresh_token：从 Redis 删除，返回 True/False
def revoke_refresh_token(jti):
    return _revoke(REFRESH_PREFIX, jti)


### 通用注销（不区分类型，两个前缀都清）：登出时只拿到 jti 可用它
def revoke_token(jti):
    return revoke_access_token(jti) and revoke_refresh_token(jti)


# ============================================================
# 刷新：用 refresh_token 换新 access_token（+ refresh 轮转）
# ============================================================

### 用 refresh_token 换新 token：校验旧 refresh → 发新 access + 新 refresh → 吊销旧 refresh
def refresh_token(old_refresh_token):
    payload = verify_refresh_token(old_refresh_token)

    # 构造简易 user 对象喂给 make_*_token
    class _UserProxy:
        pass

    user = _UserProxy()
    user.id = payload['user_id']
    user.username = payload['username']
    user.role = payload['role']

    # 发新 access
    access = make_access_token(user)
    # 轮转：同时发新 refresh，并吊销旧 refresh
    refresh = make_refresh_token(user)

    old_jti = payload.get('jti')
    if old_jti:
        revoke_refresh_token(old_jti)

    # 防重放：旧 refresh 被吊销后，若同一 refresh 再次被用来刷新，
    # verify_refresh_token 会因 Redis 已删除而抛 TOKEN_REVOKED，从而阻断。
    # 如需更强策略（检测到重放即吊销该用户全部会话），可在此扩展。

    return {'access': access['token'], 'refresh': refresh['token']}


# ============================================================
# 装饰器
# ============================================================

def _extract_bearer_token():
    """从 Authorization 头解析 'Bearer <token>'，缺失 / 格式错抛 AppError"""
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        raise AppError(code=ApiResponse.LOGIN_REQUIRED, message='请先登录')
    return auth[7:]


### token 装饰器：普通登录用户
def header_check_token_user(f):
    @wraps(f)
    def check_token(*args, **kwargs):
        token = _extract_bearer_token()
        payload = verify_access_token(token)
        g.current_user = payload        # 业务层用 g.current_user['user_id'] 取当前用户
        return f(*args, **kwargs)

    return check_token


### token 装饰器：管理员（校验 access 基础上，按需在此补充角色判断）
def header_check_token_admin(f):
    @wraps(f)
    def check_token(*args, **kwargs):
        token = _extract_bearer_token()
        payload = verify_access_token(token)
        g.current_user = payload
        # TODO: 在此校验 g.current_user['role'] 是否为管理员角色


        return f(*args, **kwargs)

    return check_token
