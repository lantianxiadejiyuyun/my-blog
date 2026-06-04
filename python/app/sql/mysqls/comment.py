from app.models import Comment
from app.utils import format_datetime


# 根据博客信息 获取对应的评论
def get_comments_from_article(article):
    comments = []

    for first in article.comments \
            .filter(Comment.status == 1, Comment.parent_id.is_(None)) \
            .order_by(Comment.created_at.desc()) \
            .all():
        comments.append({
            'id': first.id,
            'user_id': first.user_id,
            'content': first.content,
            'created_at': format_datetime(first.created_at),
            'replies': [
                {
                    'id': second.id,
                    'user_id': second.user_id,
                    'content': second.content,
                    'created_at': format_datetime(second.created_at),
                }
                for second in first.replies.filter(Comment.status == 1).all()
            ],
        })

    return comments