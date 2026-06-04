# 配置检查单

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
