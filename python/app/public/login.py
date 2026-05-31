# 登录api 三端共用
from flask import Blueprint, jsonify


login = Blueprint('login', __name__)

@login.route('/')
def index():
    return jsonify('hello world')