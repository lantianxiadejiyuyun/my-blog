# 导入核心
import logging
import os
import sys

from flask import Flask
from app.health import health
from utils import checkStart, logger as env_logger

# 检查环境变量
if not checkStart():
    env_logger.error('缺少必填环境变量，无法启动')
    sys.exit(1)

app = Flask(__name__)
app.config.from_object(__name__)  # 从当前模块加载大写配置

DEBUG = True
TESTING = True



# 路由注册
app.register_blueprint(health, url_prefix='/healthy')

# 启动
if __name__ == '__main__':
    app.run(debug=True)

