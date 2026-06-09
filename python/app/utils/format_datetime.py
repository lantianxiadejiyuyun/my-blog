import time


# 时间格式化
def format_datetime(dt):
    """datetime 对象 → '2026-6-4 21:19:22'"""
    return f'{dt.year}-{dt.month}-{dt.day} {dt.strftime("%H:%M:%S")}'

# 获取当前时间戳
def get_now_str():
    return int(time.time())