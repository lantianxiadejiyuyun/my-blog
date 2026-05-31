# 导入核心
import sys
import os

# 三方包
from dotenv import load_dotenv

from utils import checkStart, logger as env_logger

# Flask 核心程序
from flask import Flask
from app.public import register_blueprints

# 加载env环境 强制覆盖
load_dotenv(verbose=True)

# 检查环境变量
if not checkStart():
    env_logger.error('缺少必填环境变量，无法启动')
    sys.exit(1)

# Flask 配置
class FlaskConfig :
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', False)
    FLASK_PORT = os.environ.get('FLASK_PORT', 5000)

# 启动
app = Flask(__name__)

# 注册路由
register_blueprints(app)



if __name__ == '__main__':
    app.run(debug=FlaskConfig.FLASK_DEBUG,port=FlaskConfig.FLASK_PORT)

