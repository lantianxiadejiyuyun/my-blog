from app.sql.mysqls import tag as tag_db
from flask import Blueprint, jsonify

tags = Blueprint('tags', __name__)

# 获取tags 列表
@tags.route('/list', methods=['GET'])
def get_tags_list():
    tag_list = tag_db.get_tags_list()

    return jsonify({
        'tags': tag_list
    })