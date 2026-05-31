from  flask import Blueprint, jsonify

blog = Blueprint('blog', __name__)

@blog.route('/list')
def list():
    return jsonify({
        'status': 'ok',
    })
