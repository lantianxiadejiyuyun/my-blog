from app.models import User
from app.utils.format_datetime import format_datetime
from app.utils.errors import AppError
from app.extensions import db

# 最大登录失败次数
MAX_LOGIN_ATTEMPTS = 15


def get_user_login(username, password):
    """验证用户名密码登录
    成功 → 返回 user，重置 check_number
    失败 → 返回 None，递增 check_number
    锁定 → check_number >= 15 时抛 AppError
    """

    user = User.query.filter_by(username=username).first()

    # 用户不存在，直接返回 None（不暴露"用户名不存在"）
    if not user:
        return None

    # 账号被禁用
    if user.status == 0:
        raise AppError(code=1003, message='账号已被禁用，请联系管理员')

    # 登录失败次数过多，账号暂时锁定
    if user.check_number >= MAX_LOGIN_ATTEMPTS:
        raise AppError(code=1004, message=f'登录失败次数过多，账号已锁定，请联系管理员重置')

    # 密码正确：重置失败次数，返回用户
    if user.check_password(password):
        if user.check_number > 0:
            user.check_number = 0
            db.session.commit()
        return user

    # 密码错误：递增失败次数
    user.check_number += 1
    remaining = MAX_LOGIN_ATTEMPTS - user.check_number
    db.session.commit()

    if remaining > 0:
        raise AppError(code=1002, message=f'密码错误，还剩 {remaining} 次机会')
    else:
        raise AppError(code=1004, message='登录失败次数过多，账号已锁定，请联系管理员重置')
