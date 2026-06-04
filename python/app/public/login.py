# 登录api 三端共用
from flask import Blueprint, jsonify, request


login = Blueprint('login', __name__)

@login.route('/login', methods=['POST'])
def user_login():
    username = request.form['username']
    password = request.form['password']

    return jsonify('hello world')