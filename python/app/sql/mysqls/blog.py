from app.utils.validators import check_or_raise
from app.models import Article
from app.sql.mysqls.comment import get_comments_from_article
from app.utils.format_datetime import format_datetime
from app.utils.errors import AppError
from app.extensions import db

# 查询 根据页码—每页条数-查询 博客列表
def get_blog_list_from_page(page, page_size):
    page = check_or_raise(page, type='int', min_val=1, name='page')
    page_size = check_or_raise(page_size, type='int', min_val=1, max_val=100, name='page_size')

    query = Article.query
    query = query.filter(Article.status == 1)
    query = query.order_by(Article.created_at.desc())

    data = query.paginate(page=page, per_page=page_size, error_out=False)

    return {
        'list': [{
            'id': item.id,
            'title': item.title,
            'cover': item.cover,
            'category_id': item.category_id,
            'author_id': item.author_id,
            'view_count': item.view_count,
            'created_at': format_datetime(item.created_at),
            'updated_at': format_datetime(item.updated_at),
            'tags': [{'id':tags_item.id,'name':tags_item.name} for tags_item in item.tags],
        } for item in data.items],
        'page': data.page,
        'pages': data.pages,
        'total': data.total,
        'page_size': data.per_page,
    }

# 查询 根据博客id 获取 对应博客 / tags / 评论
def get_blog_detail_from_id(tag):
    id = check_or_raise(tag, type='int', min_val=1, name='id')

    query = Article.query
    query = query.filter(Article.id == id)
    query = query.filter(Article.status == 1)

    article = query.first()

    if not article:
        raise AppError(404,'未找到这个博客，请看看其他的博客吧',404)

    tags =  [{'id':item.id,'name':item.name} for item in article.tags]

    comments = get_comments_from_article(article)

    add_blog_read(article)

    return {
        'id': article.id,
        'title': article.title,
        'summary': article.summary,
        'content': article.content,
        'cover': article.cover,
        'view_count': article.view_count,
        'created_at': format_datetime(article.created_at),
        'updated_at': format_datetime(article.updated_at),
        'tags': tags,
        'comments':comments
    }

# 更新 阅读量 根据博客id 新增阅读量
def add_blog_read(article):

   article.view_count += 1
   db.session.commit()
