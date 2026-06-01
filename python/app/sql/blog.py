from app.extensions import db
from app.models import Article, Tag


def get_article_list():
    """获取文章基础查询对象"""
    return Article.query


def filter_by_status(query, status):
    """按状态筛选"""
    return query.filter(Article.status == status)


def filter_by_category(query, category_id):
    """按分类筛选"""
    return query.filter(Article.category_id == category_id)


def filter_by_tag(query, tag_id):
    """按标签筛选"""
    return query.filter(Article.tags.any(Tag.id == tag_id))


def filter_by_keyword(query, keyword):
    """关键词搜索（标题+摘要）"""
    kw = f'%{keyword}%'
    return query.filter(
        db.or_(Article.title.like(kw), Article.summary.like(kw))
    )


def order_by_created_desc(query):
    """按创建时间倒序"""
    return query.order_by(Article.created_at.desc())


def paginate(query, page, page_size):
    """分页"""
    return query.paginate(page=page, per_page=page_size, error_out=False)


def get_article_by_id(article_id):
    """文章详情"""
    return Article.query.get(article_id)


def increment_view_count(article_id):
    """阅读量+1"""
    Article.query.filter(Article.id == article_id).update(
        {Article.view_count: Article.view_count + 1}
    )
    db.session.commit()
