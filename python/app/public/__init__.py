from .login import login
from .system import system
from .blog import blog
from .tag import tags

blueprints = [
    (system, '/system'),
    (login, '/login'),
    (blog, '/blog'),
    (tags, '/tags'),
]