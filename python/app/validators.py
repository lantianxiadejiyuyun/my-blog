# ============================================================
# app/validators.py — 请求参数校验
# ============================================================
#
# 使用示例:
#
#   from app.validators import check, check_type, check_range, check_length
#
#   # ---- 统一校验 ----
#   ok, err = check('5', type='int', min_val=1, max_val=10)
#   # → (True, None)
#
#   ok, err = check('abc', type='int')
#   # → (False, '类型错误，期望 int')
#
#   ok, err = check(200, type='int', max_val=100)
#   # → (False, '值不能大于 100')
#
#   ok, err = check('hello@a.com', type='email')
#   # → (True, None)
#
#   ok, err = check('hi', type='str', min_len=5)
#   # → (False, '长度不能少于 5')
#
#   ok, err = check('draft', enum=['draft', 'published'])
#   # → (True, None)
#
#   # ---- 单独校验 ----
#   check_type(123, 'int')            # True
#   check_range(5, min_val=1)         # True
#   check_length([1,2,3], max_len=5)  # True
#
# ============================================================

import re

# 类型名 → 校验函数
_TYPE_CHECKERS = {
    'int':    lambda v: isinstance(v, int) or (isinstance(v, str) and v.lstrip('-').isdigit()),
    'float':  lambda v: isinstance(v, (int, float)) or (isinstance(v, str) and _is_float_str(v)),
    'bool':   lambda v: isinstance(v, bool) or (isinstance(v, str) and v.lower() in ('true', 'false', '1', '0')),
    'str':    lambda v: isinstance(v, str),
    'list':   lambda v: isinstance(v, list),
    'dict':   lambda v: isinstance(v, dict),
    'email':  lambda v: isinstance(v, str) and bool(re.match(r'^[^@]+@[^@]+\.[^@]+$', v)),
    'url':    lambda v: isinstance(v, str) and v.startswith(('http://', 'https://')),
    'number': lambda v: isinstance(v, (int, float)) or (isinstance(v, str) and _is_float_str(v)),
}


def _is_float_str(v):
    try:
        float(v)
        return True
    except ValueError:
        return False


def check_type(value, type_name):
    """校验 value 是否符合 type_name 类型，返回 True/False"""
    checker = _TYPE_CHECKERS.get(type_name)
    if checker is None:
        return True   # 不认识类型就不校验，默认放行
    return checker(value)


def check_range(value, min_val=None, max_val=None):
    """校验数值是否在范围内，返回 True/False

    min_val 和 max_val 至少传一个，不传的边界不检查

    示例:
        >>> check_range(5, min_val=1, max_val=10)
        True
        >>> check_range(0, min_val=1)
        False
        >>> check_range(100, max_val=50)
        False
    """
    # 先把字符串转数字
    if isinstance(value, str):
        try:
            value = float(value) if '.' in value else int(value)
        except (ValueError, TypeError):
            return False

    if not isinstance(value, (int, float)):
        return False

    if min_val is not None and value < min_val:
        return False
    if max_val is not None and value > max_val:
        return False
    return True


def check_length(value, min_len=None, max_len=None):
    """校验字符串或列表的长度是否在范围内，返回 True/False

    示例:
        >>> check_length('hello', min_len=1, max_len=10)
        True
        >>> check_length('hi', min_len=5)
        False
        >>> check_length([1,2,3], max_len=2)
        False
    """
    if not hasattr(value, '__len__'):
        return False

    length = len(value)

    if min_len is not None and length < min_len:
        return False
    if max_len is not None and length > max_len:
        return False
    return True


def check(value, type=None, min_val=None, max_val=None, min_len=None, max_len=None,
          enum=None, regex=None, validator=None, name=None):
    """统一校验入口，返回 (is_valid, error_msg)

    所有参数都是可选的，传了就校验，不传就跳过。
    传了 name 则错误信息自动带上参数名前缀，格式: "{name}: 错误原因"

    返回:
        (True, None)        — 全部通过
        (False, '错误信息')  — 某项未通过

    示例:
        >>> check('abc', type='int', name='page')
        (False, 'page: 类型错误，期望 int')

        >>> check(200, type='int', max_val=100, name='page_size')
        (False, 'page_size: 值不能大于 100')
    """
    label = f'{name}: ' if name else ''

    # 1. 类型校验
    if type is not None:
        if not check_type(value, type):
            return False, f'{label}类型错误，期望 {type}'

    # 2. 数值范围校验
    if min_val is not None or max_val is not None:
        if not check_range(value, min_val, max_val):
            reason = ''
            if min_val is not None and max_val is not None:
                reason = f'值应在 {min_val} ~ {max_val} 之间'
            elif min_val is not None:
                reason = f'值不能小于 {min_val}'
            else:
                reason = f'值不能大于 {max_val}'
            return False, f'{label}{reason}'

    # 3. 长度校验
    if min_len is not None or max_len is not None:
        if not check_length(value, min_len, max_len):
            reason = ''
            if min_len is not None and max_len is not None:
                reason = f'长度应在 {min_len} ~ {max_len} 之间'
            elif min_len is not None:
                reason = f'长度不能少于 {min_len}'
            else:
                reason = f'长度不能超过 {max_len}'
            return False, f'{label}{reason}'

    # 4. 枚举白名单
    if enum is not None and value not in enum:
        return False, f'{label}取值只能是: {enum}'

    # 5. 正则
    if regex is not None and not re.match(regex, str(value)):
        return False, f'{label}格式不合法'

    # 6. 自定义校验
    if validator is not None and callable(validator):
        ok, err = validator(value)
        if not ok:
            return False, f'{label}{err}'

    return True, None


def _cast(value, type_name):
    """把 value 转成目标类型，转换失败返回原值"""
    if type_name in ('int',):
        return int(value) if isinstance(value, str) else value
    if type_name in ('float', 'number'):
        return float(value) if isinstance(value, str) else value
    if type_name == 'bool' and isinstance(value, str):
        return value.lower() in ('true', '1')
    return value


def check_or_raise(value, type=None, min_val=None, max_val=None, min_len=None, max_len=None,
                   enum=None, regex=None, validator=None, name=None, error_code=1001):
    """校验失败抛 AppError，校验通过返回转换后的值

    跟 check() 参数完全一样，区别是：
    1. 失败不是返回 False，而是抛 AppError（被 errors.py 第一层自动接住）
    2. 通过后返回转换过的值（比如 '1' 变成 1），调用方直接用

    name 参数会在错误信息中作为前缀，保持跟前端传参名一致。

    示例:
        >>> page = check_or_raise('5', type='int', min_val=1, name='page')
        >>> page
        5

        >>> check_or_raise('abc', type='int', name='page')
        # → raise AppError(1001, 'page: 类型错误，期望 int')
    """
    from .errors import AppError

    ok, err = check(value, type=type, min_val=min_val, max_val=max_val,
                    min_len=min_len, max_len=max_len,
                    enum=enum, regex=regex, validator=validator, name=name)
    if not ok:
        raise AppError(code=error_code, message=err)

    # 校验通过，转换成目标类型再返回
    if type is not None:
        return _cast(value, type)
    return value
