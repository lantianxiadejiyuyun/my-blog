from flask import Blueprint, jsonify, request
from app.utils.validators import check_or_raise
from app.methods.token import make_token, verify_token, revoke_token
from app.sql.mysqls.user import get_user_login

user = Blueprint('user', __name__)

# 用户登入账号
@user.route('/login', methods=['POST'])
def user_login():
    username = request.form['username']
    password = request.form['password']

    check_or_raise(username,type='string',max_len=50,min_len=1,name='username')
    check_or_raise(password,type='string',max_len=200,min_len=1,name='password')

    user_data = get_user_login(username,password)

    if user_data:
        token_datas = make_token(user_data)

        return jsonify({
            'code': 200,
            'message': '登录成功',
            'token': token_datas['token'],
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

# 验证 token 是否有效
@user.route('/check', methods=['POST'])
def user_check():
    token = request.form['token']

    payload = verify_token(token)

    return jsonify({
        'code': 200,
        'message': 'Token 有效',
        'user': {
            'user_id': payload['user_id'],
            'username': payload['username'],
            'role': payload['role'],
        }
    })

# 用户登出
@user.route('/logout', methods=['POST'])
def user_logout():
    token = request.form['token']

    payload = verify_token(token)
    revoked = revoke_token(payload['jti'])

    if revoked:
        return jsonify({'code': 200, 'message': '登出成功'})
    else:
        return jsonify({'code': 500, 'message': '登出失败'})