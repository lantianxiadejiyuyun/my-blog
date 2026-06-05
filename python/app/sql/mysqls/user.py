from app.models import User
from app.utils.format_datetime import format_datetime
from app.utils.errors import AppError

def get_user_login(username, password):

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        return user
    else:
        return None
