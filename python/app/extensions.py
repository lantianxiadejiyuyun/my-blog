from flask_sqlalchemy import SQLAlchemy
import redis
from app.config import Config

db = SQLAlchemy()


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
