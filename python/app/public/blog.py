from flask import Blueprint, jsonify, request

from app.sql.mysqls.blog import *
from app.utils.validators import check_or_raise

blog = Blueprint('blog', __name__)


# 带分页的首页博客list
@blog.route('/blog_list')
def page_list():
    page = request.args.get('page', '1')
    page_size = request.args.get('page_size', '10')

    result = get_blog_list_from_page(page, page_size)
    return jsonify({
        'status': 'ok',
        'data': result,
    })


# 查询 根据博客id 获取对应的博客数据
@blog.route('/blog_detail')
def blog_detail():
    id = request.args.get('id')

    result = get_blog_detail_from_id(id)

    return jsonify({
        'status': 'ok',
        'data': result
    })
