from flask import Blueprint, jsonify, request
from app.sql.mysqls.blog import get_blog_list_from_page
blog = Blueprint('blog', __name__)

# 带分页的首页博客list
@blog.route('/list')
def page_list():
    page = request.args.get('page', '1')
    page_size = request.args.get('page_size', '10')

    result = get_blog_list_from_page(page, page_size)
    return jsonify({
        'status': 'ok',
        'data': result,
    })
