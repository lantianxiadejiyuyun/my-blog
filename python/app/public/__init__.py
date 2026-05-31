from .login import login
from .health import health
from .blog import blog

blueprints = [
    (health, '/health'),
    (login, '/login'),
    (blog, '/blog'),
]