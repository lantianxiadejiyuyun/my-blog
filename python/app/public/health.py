import psutil
from flask import Blueprint, jsonify

health = Blueprint('health', __name__)


# 检查cpu使用率 内存 硬盘
@health.route('/check')
def check():
    return jsonify({
        'cpu': {
            'percent': psutil.cpu_percent(interval=0.5),
            'count': psutil.cpu_count(),
        },
        'memory': {
            'total': psutil.virtual_memory().total,
            'used': psutil.virtual_memory().used,
            'percent': psutil.virtual_memory().percent,
        },
        'disk': {
            'total': psutil.disk_usage('/').total,
            'used': psutil.disk_usage('/').used,
            'percent': psutil.disk_usage('/').percent,
        },
    })

