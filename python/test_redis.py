"""
Redis 连接测试脚本
用法：在 python 目录下运行 python test_redis.py
"""
import os
import socket
import sys

# 加载 .env
from dotenv import load_dotenv
load_dotenv()

print('=' * 50)
print('Redis 连接测试')
print('=' * 50)

HOST = os.environ.get('REDIS_HOST')
PORT = os.environ.get('REDIS_PORT')
PASSWORD = os.environ.get('REDIS_PASSWORD') or None
DB_SESSION = os.environ.get('REDIS_DB_SESSION', '0')
DB_CACHE = os.environ.get('REDIS_DB_CACHE', '1')
DB_RATELIMIT = os.environ.get('REDIS_DB_RATELIMIT', '2')

print(f'\n📋 读取到的配置:')
print(f'   HOST={HOST}')
print(f'   PORT={PORT}')
print(f'   PASSWORD={PASSWORD!r}')
print(f'   DB_SESSION={DB_SESSION}')
print(f'   DB_CACHE={DB_CACHE}')
print(f'   DB_RATELIMIT={DB_RATELIMIT}')

# ---- 第1步：TCP 通不通 ----
print(f'\n--- 第1步：TCP 连接测试 ---')
try:
    sock = socket.create_connection((HOST, int(PORT)), timeout=5)
    sock.close()
    print(f'✅ {HOST}:{PORT} TCP 端口通')
except Exception as e:
    print(f'❌ {HOST}:{PORT} TCP 端口不通: {e}')
    print('   → 检查：Redis 服务状态、防火墙、端口号对不对')
    sys.exit(1)

# ---- 第2步：能连上 Redis 吗 ----
print(f'\n--- 第2步：Redis 客户端连接 ---')
try:
    import redis
    r = redis.Redis(
        host=HOST,
        port=int(PORT),
        password=PASSWORD,
        decode_responses=True,
        socket_connect_timeout=5,
    )
    ping_result = r.ping()
    print(f'✅ ping() → {ping_result}，连接成功')
except redis.ConnectionError as e:
    print(f'❌ 连接失败: {e}')
    print('   → 检查：密码对不对、Redis 是否在正确的端口监听')
    sys.exit(1)

# ---- 第3步：三个 db 能切吗 ----
print(f'\n--- 第3步：测试三个 db ---')
dbs = {
    'DB_SESSION': int(DB_SESSION),
    'DB_CACHE': int(DB_CACHE),
    'DB_RATELIMIT': int(DB_RATELIMIT),
}

for name, db_num in dbs.items():
    try:
        test_r = redis.Redis(
            host=HOST,
            port=int(PORT),
            password=PASSWORD,
            db=db_num,
            decode_responses=True,
            socket_connect_timeout=5,
        )
        test_r.ping()
        # 写入一个测试 key，马上删掉
        test_key = '__test_connection__'
        test_r.set(test_key, '1', ex=10)
        val = test_r.get(test_key)
        test_r.delete(test_key)

        if val == '1':
            print(f'✅ {name} (db={db_num}) 读写正常')
        else:
            print(f'⚠️  {name} (db={db_num}) 连接正常但 get 返回了 {val!r}')
    except Exception as e:
        print(f'❌ {name} (db={db_num}) 错误: {e}')

# ---- 第4步：看下 Redis 信息 ----
print(f'\n--- 第4步：Redis 基本信息 ---')
try:
    info = r.info('server')
    print(f'   Redis 版本: {info["redis_version"]}')
    print(f'   运行模式: {info["redis_mode"]}')
    print(f'   运行时间: {info["uptime_in_seconds"]} 秒')
except Exception as e:
    print(f'   获取 info 失败: {e}')

# ---- 第5步：显示所有 db 的 key 数量 ----
print(f'\n--- 第5步：各库 key 数量 ---')
for i in range(4):
    try:
        count_r = redis.Redis(
            host=HOST, port=int(PORT), password=PASSWORD, db=i,
            decode_responses=True, socket_connect_timeout=5,
        )
        size = count_r.dbsize()
        print(f'   db{i}: {size} 个 key')
    except Exception as e:
        print(f'   db{i}: 错误 - {e}')

print(f'\n{"=" * 50}')
print('测试完成')
print('=' * 50)
