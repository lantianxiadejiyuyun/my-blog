import os

class Config:
    # Mysql
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
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD') or None
    REDIS_PORT = int(os.environ.get('REDIS_PORT'))

    REDIS_DB_SESSION = os.environ.get('REDIS_DB_SESSION')
    REDIS_DB_CACHE = os.environ.get('REDIS_DB_CACHE')
    REDIS_DB_RATELIMIT = os.environ.get('REDIS_DB_RATELIMIT')
    REDIS_DB_QUEUE = os.environ.get('REDIS_DB_QUEUE')

    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_EXPIRES = os.environ.get('JWT_ACCESS_EXPIRES')
    JWT_REFRESH_EXPIRES = os.environ.get('JWT_REFRESH_EXPIRES')

    # 用户最大校验次数
    MAX_LOGIN_ATTEMPTS = int(os.environ.get('MAX_LOGIN_ATTEMPTS'))
