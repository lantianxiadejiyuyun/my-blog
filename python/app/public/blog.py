from flask import Blueprint, jsonify, request
from app.sql.mysqls.blog import paginate,get_article_list

blog = Blueprint('blog', __name__)

# 带分页的首页博客list
@blog.route('/list')
def list():
    page = request.args.get('page', 1, type=int)
    total = request.args.get('total', 10, type=int)
    page_size = request.args.get('page_size', 10, type=int)

    query = paginate(get_article_list,page,total)


    return jsonify({
        'status': query,
    })
