# ============================================================
# app/response.py — 统一响应封装
# ============================================================
from flask import jsonify


class ApiResponse:
    """
    业务状态码规范
    ────────────────
    编码规则：模块号(2位) + 序号(2位)，从 1000 起，避免与 HTTP 状态码混淆

    模块划分：
      10xx  通用 / 参数
      11xx  认证（登录 / 注册 / 登出）
      12xx  Token / 权限
      20xx  文章
      21xx  分类
      22xx  标签
      23xx  评论
      24xx  用户管理
      30xx  文件上传
      31xx  限流
    """

    # ==================================================================
    # HTTP 协议层（直接复用 HTTP 状态码，不自定义）
    # ==================================================================
    SUCCESS = 200               # 请求成功
    CREATED = 201               # 资源创建成功
    NO_CONTENT = 204            # 请求成功，无返回内容（如删除成功）
    BAD_REQUEST = 400           # 请求参数错误（通用兜底）
    UNAUTHORIZED = 401          # 未认证（没带 token）
    FORBIDDEN = 403             # 无权限（token 有效但角色不够）
    NOT_FOUND = 404             # 路由 / 资源不存在
    METHOD_NOT_ALLOWED = 405    # 请求方法不允许
    CONFLICT = 409              # 资源冲突（如重复注册）
    UNPROCESSABLE = 422         # 参数格式正确但语义错误
    TOO_MANY_REQUESTS = 429     # 请求过于频繁（限流）
    SERVER_ERROR = 500          # 服务器内部错误

    # ==================================================================
    # 10xx — 通用 / 参数错误
    # ==================================================================
    PARAM_MISSING = 1000        # 缺少必填参数
    PARAM_INVALID = 1001        # 参数格式错误（如 page 传了字符串）
    PARAM_VALUE_RANGE = 1002    # 参数值超出允许范围（如 page_size > 100）
    PARAM_TYPE_ERROR = 1003     # 参数类型错误（如该传数组的传了字符串）
    RESOURCE_LOCKED = 1004      # 资源被锁定（乐观锁冲突，请重试）
    OPERATION_FAILED = 1005     # 操作失败（通用兜底，非特定业务错误）
    PAGE_OUT_OF_RANGE = 1006    # 分页页码超出范围（请求的 page 大于总页数）
    DATA_VALIDATION_FAILED = 1007  # 数据校验失败（如 JSON Schema 校验不通过）

    # ==================================================================
    # 11xx — 认证模块（登录 / 注册 / 登出）
    # ==================================================================
    USER_NOT_EXIST = 1100       # 用户不存在
    PASSWORD_WRONG = 1101       # 密码错误
    USER_BANNED = 1102          # 账号已被禁用
    USERNAME_TAKEN = 1103       # 用户名已被占用
    EMAIL_TAKEN = 1104          # 邮箱已被注册
    REGISTER_FAILED = 1105      # 注册失败（数据库写入失败等）
    NICKNAME_REQUIRED = 1106    # 游客身份缺少昵称（非登录用户操作时）
    OLD_PASSWORD_WRONG = 1107   # 旧密码错误（修改密码 / 修改邮箱时校验身份）
    PASSWORD_TOO_WEAK = 1108    # 密码强度不足（长度不够 / 缺少字母数字特殊字符等）
    USERNAME_FORMAT_INVALID = 1109  # 用户名格式不合法（含特殊字符 / 长度超出 / 纯数字等）
    EMAIL_FORMAT_INVALID = 1110     # 邮箱格式不合法

    # ==================================================================
    # 12xx — Token / 权限
    # ==================================================================
    TOKEN_EXPIRED = 1200        # access_token 过期，需用 refresh_token 换新
    TOKEN_INVALID = 1201        # token 无效（伪造 / 被篡改 / 已登出）
    NO_PERMISSION = 1202        # 当前角色无此操作权限（admin 试图改 serveradmin）
    LOGIN_REQUIRED = 1203       # 需要登录（请求未携带 token）
    TOKEN_REVOKED = 1204        # token 已被主动吊销（服务端做了登出）
    REFRESH_TOKEN_EXPIRED = 1205  # refresh_token 也过期了，需重新登录
    REFRESH_TOKEN_INVALID = 1206  # refresh_token 无效
    NOT_OWNER = 1207            # 不是资源所有者（只能操作自己的数据，如删除他人的评论）
    TOKEN_IS_NOT_SAVE = 1208    # token 保存失败

    # ==================================================================
    # 20xx — 文章模块
    # ==================================================================
    ARTICLE_NOT_EXIST = 2000    # 文章不存在
    ARTICLE_DRAFT = 2001        # 文章为草稿状态，无权查看
    ARTICLE_BANNED = 2002       # 文章已被屏蔽
    ARTICLE_CREATE_FAILED = 2003  # 文章创建失败
    ARTICLE_UPDATE_FAILED = 2004  # 文章更新失败
    ARTICLE_DELETE_FAILED = 2005  # 文章删除失败
    ARTICLE_TITLE_TAKEN = 2006  # 文章标题已存在
    ARTICLE_ALREADY_PUBLISHED = 2007  # 文章已发布，无需重复操作
    ARTICLE_CONTENT_EMPTY = 2008   # 文章内容为空（创建 / 更新时）

    # ==================================================================
    # 21xx — 分类模块
    # ==================================================================
    CATEGORY_NOT_EXIST = 2100   # 分类不存在
    CATEGORY_NAME_TAKEN = 2101  # 分类名已存在
    CATEGORY_HAS_ARTICLES = 2102  # 分类下仍有文章，不可删除
    CATEGORY_CREATE_FAILED = 2103  # 分类创建失败
    CATEGORY_UPDATE_FAILED = 2104  # 分类更新失败
    CATEGORY_DELETE_FAILED = 2105  # 分类删除失败

    # ==================================================================
    # 22xx — 标签模块
    # ==================================================================
    TAG_NOT_EXIST = 2200        # 标签不存在
    TAG_NAME_TAKEN = 2201       # 标签名已存在
    TAG_CREATE_FAILED = 2202    # 标签创建失败
    TAG_UPDATE_FAILED = 2203    # 标签更新失败
    TAG_DELETE_FAILED = 2204    # 标签删除失败

    # ==================================================================
    # 23xx — 评论模块
    # ==================================================================
    COMMENT_NOT_EXIST = 2300    # 评论不存在
    COMMENT_EMPTY = 2301        # 评论内容为空
    COMMENT_TOO_FREQUENT = 2302 # 评论过于频繁（10 秒内重复提交）
    COMMENT_CLOSED = 2303       # 文章已关闭评论
    COMMENT_DELETE_FAILED = 2304  # 评论删除失败
    NOT_YOUR_COMMENT = 2305     # 无权删除他人的评论（非本人且非管理员）
    COMMENT_STATUS_INVALID = 2306  # 评论状态流转不合法（如已通过的评论再次审核）
    COMMENT_NEED_REVIEW = 2307  # 评论需要审核（提示用户"评论已提交，等待审核"）
    COMMENT_CONTENT_TOO_LONG = 2308   # 评论内容超过字数限制
    PARENT_COMMENT_DELETED = 2309     # 被回复的父评论已被删除

    # ==================================================================
    # 24xx — 用户管理模块
    # ==================================================================
    USER_PROFILE_NOT_EXIST = 2400  # 用户信息不存在
    CANNOT_MODIFY_SELF_ROLE = 2401  # 不能修改自己的角色
    CANNOT_MODIFY_HIGHER_ROLE = 2402  # 不能修改同级或更高级角色
    CANNOT_BAN_SELF = 2403      # 不能禁用自己
    CANNOT_BAN_HIGHER = 2404    # 不能禁用同级或更高级用户
    USER_UPDATE_FAILED = 2405   # 用户信息更新失败
    ROLE_NOT_EXIST = 2406       # 目标角色不存在（传了非法的角色名）

    # ==================================================================
    # 30xx — 文件上传
    # ==================================================================
    FILE_TOO_LARGE = 3000       # 文件超过大小限制
    FILE_TYPE_DENIED = 3001     # 文件类型不允许
    FILE_UPLOAD_FAILED = 3002   # 文件上传失败
    FILE_NOT_EXIST = 3003       # 文件不存在（访问了已删除的文件）

    # ==================================================================
    # 31xx — 限流
    # ==================================================================
    RATE_LIMITED = 3100         # 全局限流（请求过于频繁，请稍后再试）
    LOGIN_TOO_FREQUENT = 3101   # 登录过于频繁（防暴力破解）
    REGISTER_TOO_FREQUENT = 3102  # 注册过于频繁（防机器批量注册）


# ==================================================================
# 响应工具函数
# ==================================================================

def success(data=None, message='ok', code=ApiResponse.SUCCESS):
    """成功响应"""
    return jsonify({
        'code': code,
        'message': message,
        'data': data or {},
    }), 200 if code in (200, 201, 204) else code


def fail(code, message, data=None, http_status=None):
    """失败响应"""
    return jsonify({
        'code': code,
        'message': message,
        'data': data or {},
    }), http_status or 400


def paginate_response(items, page, page_size, total):
    """分页响应"""
    return jsonify({
        'code': 200,
        'message': 'ok',
        'data': {
            'list': items,
            'page': page,
            'page_size': page_size,
            'total': total,
            'total_page': (total + page_size - 1) // page_size,
        },
    })
