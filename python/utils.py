import os
import logging

logger = logging.getLogger(__name__)


class checkConfig:
    DB_PORT = os.environ.get('DB_PORT', '')
    DB_USER = os.environ.get('DB_USER', '')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_HOST = os.environ.get('DB_HOST', '')
    DB_NAME = os.environ.get('DB_NAME', '')

    REDIS_HOST = os.environ.get('REDIS_HOST', '')
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', '')
    REDIS_DB = os.environ.get('REDIS_DB', '')

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', '')
    JWT_ACCESS_EXPIRES = os.environ.get('JWT_ACCESS_EXPIRES', '')
    FLASK_ENV = os.environ.get('FLASK_ENV', '')


def checkStart():
    required = [
        ('DB_PORT',            checkConfig.DB_PORT),
        ('DB_USER',            checkConfig.DB_USER),
        ('DB_PASSWORD',        checkConfig.DB_PASSWORD),
        ('DB_HOST',            checkConfig.DB_HOST),
        ('DB_NAME',            checkConfig.DB_NAME),
        ('REDIS_HOST',         checkConfig.REDIS_HOST),
        ('REDIS_PASSWORD',     checkConfig.REDIS_PASSWORD),
        ('JWT_SECRET_KEY',     checkConfig.JWT_SECRET_KEY),
        ('JWT_ACCESS_EXPIRES', checkConfig.JWT_ACCESS_EXPIRES),
        ('FLASK_ENV',          checkConfig.FLASK_ENV),
        ('REDIS_DB',           checkConfig.REDIS_DB),
    ]

    missing = [name for name, value in required if not value]

    if missing:
        logger.error('缺少必填环境变量: %s', ', '.join(missing))
        return False
    return True