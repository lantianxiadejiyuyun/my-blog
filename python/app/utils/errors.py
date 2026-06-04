# ============================================================
# app/utils/errors.py — 全局异常处理
# ============================================================
from werkzeug.exceptions import HTTPException

from app.utils.response import fail


# ========== 自定义业务异常 ==========
class AppError(Exception):
    """在业务代码里主动抛出，带上业务码和中文提示"""
    def __init__(self, code, message, http_code=400):
        self.code = code
        self.message = message
        self.http_code = http_code


# ========== 注册错误处理器 ==========
def register_error_handlers(app):
    """三层错误捕获，按 AppError → HTTPException → Exception 优先级递减匹配"""

    # 第1层：你主动抛出的业务异常
    @app.errorhandler(AppError)
    def handle_app_error(e):
        return fail(e.code, e.message, http_status=e.http_code)

    # 第2层：Flask/Werkzeug 自己的 HTTP 异常（404、405、500 等）
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return fail(e.code or 500, e.description, http_status=e.code or 500)

    # 第3层：兜底，所有没被上面两层接住的未知异常
    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        app.logger.exception('未捕获的异常')
        return fail(500, '服务器内部错误，请稍后重试', http_status=500)
