from app.utils.validators import check_or_raise
from app.models import Tag
from app.utils.errors import AppError

# 获取tags 列表
def get_tags_list():
    tags = Tag.query.all()

    return [{'id': tag.id, 'name': tag.name} for tag in tags]