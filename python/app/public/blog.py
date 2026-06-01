from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import User

blog = Blueprint('blog', __name__)

@blog.route('/list')
def list(page,total,):
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page', 1, type=int)

    # 查询数据库

    return jsonify({
        'status': 'ok',
    })
