import os
import logging

logger = logging.getLogger(__name__)


class CheckConfig:
    DB_PORT = os.getenv('DB_PORT', '')
    DB_USER = os.getenv('DB_USER', '')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_HOST = os.getenv('DB_HOST', '')
    DB_NAME = os.getenv('DB_NAME', '')

    REDIS_HOST = os.getenv('REDIS_HOST', '')
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
    REDIS_PORT = os.getenv('REDIS_PORT', '')
    REDIS_DB = os.getenv('REDIS_DB', '')

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '')
    JWT_ACCESS_EXPIRES = os.getenv('JWT_ACCESS_EXPIRES', '')

    FLASK_ENV = os.getenv('FLASK_ENV', '')
    FLASK_PORT = os.getenv('FLASK_PORT', '')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', '')

def checkStart():
    required = [
        ('DB_PORT',            CheckConfig.DB_PORT),
        ('DB_USER',            CheckConfig.DB_USER),
        ('DB_PASSWORD',        CheckConfig.DB_PASSWORD),
        ('DB_HOST',            CheckConfig.DB_HOST),
        ('DB_NAME',            CheckConfig.DB_NAME),

        ('REDIS_HOST',         CheckConfig.REDIS_HOST),
        ('REDIS_PORT',         CheckConfig.REDIS_PORT),
        ('REDIS_PASSWORD',     CheckConfig.REDIS_PASSWORD),
        ('REDIS_DB',           CheckConfig.REDIS_DB),

        ('JWT_SECRET_KEY',     CheckConfig.JWT_SECRET_KEY),
        ('JWT_ACCESS_EXPIRES', CheckConfig.JWT_ACCESS_EXPIRES),

        ('FLASK_ENV',          CheckConfig.FLASK_ENV),
        ('FLASK_PORT',         CheckConfig.FLASK_PORT),
        ('FLASK_DEBUG',        CheckConfig.FLASK_DEBUG),
    ]

    missing = [name for name, value in required if not value]

    if missing:
        logger.error('缺少必填环境变量: %s', ', '.join(missing))
        return False
    return True