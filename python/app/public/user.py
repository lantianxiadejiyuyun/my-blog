# 登录api 三端共用
from flask import Blueprint, jsonify, request
from app.utils.validators import check_or_raise
from app.methods.token import make_token
from app.sql.mysqls.user import get_user_login

user = Blueprint('user', __name__)

@user.route('/login', methods=['POST'])
def user_login():
    username = request.form['username']
    password = request.form['password']

    check_or_raise(username,type='string',max_len=50,min_len=1,name='username')
    check_or_raise(password,type='string',max_len=200,min_len=1,name='password')

    user_data = get_user_login(username,password)

    if user_data:
        token = make_token(user_data)

        return jsonify({
            'code': 200,
            'message': '登录成功',
            'token': token,
            'user': {
                'username': user_data.username,
                'id': user_data.id,
                'email': user_data.email,
                'avatar': user_data.avatar,
                'bio': user_data.bio,
                'status': user_data.status,
                'created_at': user_data.created_at.isoformat() if user_data.created_at else None,
            }
        })

    else:
        return jsonify({"message":'登录失败'})
