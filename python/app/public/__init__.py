from .user import user
from .system import system
from .blog import blog
from .tag import tags
from .carousel import carousel

blueprints = [
    (system, '/system'),
    (user, '/user'),
    (blog, '/blog'),
    (tags, '/tags'),
    (carousel, '/carousel'),
]