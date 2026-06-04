from flask import Blueprint, jsonify, request

from app.sql.mysqls import blog as blog_db

blog = Blueprint('blog', __name__)


# 带分页的首页博客list
@blog.route('/list')
def get_blog_list_from_page():
    page = request.args.get('page', '1')
    page_size = request.args.get('page_size', '10')

    result = blog_db.get_blog_list_from_page(page, page_size)
    return jsonify({
        'status': 'ok',
        'data': result,
    })


# 查询 根据博客id 获取对应的博客数据
@blog.route('/detail')
def get_blog_detail_from_id():
    id = request.args.get('id')

    result = blog_db.get_blog_detail_from_id(id)

    return jsonify({
        'status': 'ok',
        'data': result
    })
