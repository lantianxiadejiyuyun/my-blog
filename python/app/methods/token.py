from datetime import datetime, timezone
import jwt
from app.config import Config
import os
import uuid
from app.utils.errors import AppError


# 检查token
def check_token(token):

    jwt_token = jwt.decode(token, Config.JWT_SECRET_KEY, algorithm=['HS256'])
    print('jwt',jwt_token)

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
        'jti': mark_uuid(), # 构建uuid
        'role': user.role, # 权限
        'iat': now,  # 签发时间
        'exp': int(os.environ.get('JWT_ACCESS_EXPIRES') or 1800) # 过期延后
    }

    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

# 长效token uuid
def mark_uuid():
    return str(uuid.uuid4())

# 重新保存token
def refresh_token():

    return

# 删除token
def delete_token():

    return

