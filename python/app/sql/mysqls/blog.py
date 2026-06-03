from app.validators import check_or_raise
from app.models import Article, Tag


# 查询 根据页码—每页条数-查询 博客列表
def get_blog_list_from_page(page, page_size):
    page = check_or_raise(page, type='int', min_val=1, name='page')
    page_size = check_or_raise(page_size, type='int', min_val=1, max_val=100, name='page_size')

    query = Article.query
    query = query.filter(Article.status == 1)
    query = query.order_by(Article.created_at.desc())

    data = query.paginate(page=page, per_page=page_size, error_out=False)

    return {
        'list': [{'id': item.id, 'title': item.title} for item in data.items],
        'page': data.page,
        'pages': data.pages,
        'total': data.total,
        'page_size': data.per_page,
    }