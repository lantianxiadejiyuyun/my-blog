from .user import user
from .system import system
from .blog import blog
from .tag import tags

blueprints = [
    (system, '/system'),
    (user, '/user'),
    (blog, '/blog'),
    (tags, '/tags'),
]