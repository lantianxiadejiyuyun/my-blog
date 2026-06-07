from datetime import datetime, timezone
import jwt
from app.config import Config
import os

# 检查token
def check_token():

    return

# 保存用户token
def save_token():

    return

# 计算token
def make_token(user):
    """ 生成用户 totken """
    now = datetime.now(timezone.utc)
    payload = {
        'user_id': user.id,
        'username': user.username,
        'role': user.role,
        'iat': now,
        'exp': int(os.environ.get('JWT_ACCESS_EXPIRES') or 1800)
    }

    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

def parse_token(token):
    """校验 token，成功返回 payload，失败抛 jwt 异常"""
    return jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])


def mark_uuid():

    return 


# 重新保存token
def refresh_token():

    return

# 删除token
def delete_token():

    return

