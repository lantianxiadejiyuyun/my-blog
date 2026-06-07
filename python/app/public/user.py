# 登录api 三端共用
from flask import Blueprint, jsonify, request
from app.utils.validators import check_or_raise


user = Blueprint('user', __name__)

@user.route('/login', methods=['POST'])
def user_login():
    username = request.form['username']
    password = request.form['password']

    check_or_raise(username,type='string',max_len=50,min_len=1,name='username')
    check_or_raise(password,type='string',max_len=200,min_len=1,name='password')



    return jsonify('hello world')
