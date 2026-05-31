# 配置检查单

import os
import logging

logger = logging.getLogger(__name__)

def checkStart():
    required = [
        ('DB_HOST', os.getenv('DB_HOST')),
        ('DB_PORT', os.getenv('DB_PORT')),
        ('DB_USER', os.getenv('DB_USER')),
        ('DB_PASSWORD', os.getenv('DB_PASSWORD')),
        ('DB_NAME', os.getenv('DB_NAME')),
        ('REDIS_HOST', os.getenv('REDIS_HOST')),
        ('REDIS_PORT', os.getenv('REDIS_PORT')),
        ('REDIS_PASSWORD', os.getenv('REDIS_PASSWORD')),
        ('REDIS_DB', os.getenv('REDIS_DB')),
        ('JWT_SECRET_KEY', os.getenv('JWT_SECRET_KEY')),
        ('JWT_ACCESS_EXPIRES', os.getenv('JWT_ACCESS_EXPIRES')),
        ('FLASK_ENV', os.getenv('FLASK_ENV')),
        ('FLASK_PORT', os.getenv('FLASK_PORT')),
        ('FLASK_DEBUG', os.getenv('FLASK_DEBUG')),
    ]

    missing = [name for name, value in required if not value]

    if missing:
        logger.error('缺少必填环境变量: %s', ', '.join(missing))
        return False

    return True
