from app.utils.validators import check_or_raise
from app.models import Article, Tag, Comment
from app.sql.mysqls.comment import get_comments_from_article
from app.utils.errors import AppError

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

# 查询 根据博客id 获取 对应博客 / tags / 评论
def get_blog_detail_from_id(id):
    id = check_or_raise(id, type='int', min_val=1, name='id')

    query = Article.query
    query = query.filter(Article.id == id)
    query = query.filter(Article.status == 1)

    article = query.first()
    if not article:
        raise AppError(404,'未找到这个博客，请看看其他的博客吧',404)

    tags =  [{'id':item.id,'name':item.name} for item in article.tags]

    comments = get_comments_from_article(article)

    return {
        'id': article.id,
        'title': article.title,
        'summary': article.summary,
        'content': article.content,
        'cover': article.cover,
        'view_count': article.view_count,
        'created_at': article.created_at,
        'updated_at': article.updated_at,
        'tags': tags ,
        'comments':comments
    }