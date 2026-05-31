# 统一注册
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from .public import blueprints as public_bps
from .config import Config


API_PREFIX = '/api'

def register_blueprints(app):
    for bp,prefix in public_bps:
        app.register_blueprint(bp,url_prefix=f'{API_PREFIX}/{prefix}')


# 项目初始化
db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    register_blueprints(app)
    CORS(app)

    return app