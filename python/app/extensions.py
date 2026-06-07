from flask_sqlalchemy import SQLAlchemy
import redis
from app.config import Config

db = SQLAlchemy()


redis_session = None
redis_cache = None
redis_ratelimit = None


def _make_redis(app, db_key):
    """内部工具：根据 db_key 创建 Redis 连接"""
    return redis.Redis(
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT'],
        password=app.config['REDIS_PASSWORD'],
        db=app.config[db_key],
        decode_responses=True,
        socket_connect_timeout=5,
    )


def init_redis(app):
    """在 create_app() 里调用，一次性初始化三个连接"""
    global redis_session, redis_cache, redis_ratelimit

    redis_session = _make_redis(app, 'REDIS_DB_SESSION')
    redis_cache = _make_redis(app, 'REDIS_DB_CACHE')
    redis_ratelimit = _make_redis(app, 'REDIS_DB_RATELIMIT')

    # 验证一下
    try:
        redis_session.ping()
        redis_cache.ping()
        redis_ratelimit.ping()
    except redis.ConnectionError as e:
        raise RuntimeError(f'Redis 连不上，检查地址和密码: {e}')