from flask import Flask

from .login import login
from .health import health
from .blog import blog

def register_blueprints(app):
    app.register_blueprint(health, url_prefix='/health')
    app.register_blueprint(login, url_prefix='/login')
    app.register_blueprint(blog, url_prefix='/blog')
