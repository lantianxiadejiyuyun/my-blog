# 项目入口
from flask_cors import CORS
from flask import Flask

from .public import blueprints as public_bps
from .config import Config
from .extensions import db
from .errors import register_error_handlers


API_PREFIX = '/api'

def register_blueprints(app):
    for bp,prefix in public_bps:
        app.register_blueprint(bp,url_prefix=f'{API_PREFIX}/{prefix}')


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    register_blueprints(app)
    register_error_handlers(app)
    CORS(app)

    return app