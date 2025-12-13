from redis import ConnectionPool, Redis


def redis_client():
    pool = ConnectionPool(
        host='localhost',
        port=6379, # Redis 預設 Port（可改）
        password=None,
        decode_responses=True,  # 自動把 bytes 轉成字串
        max_connections=10
    )

    return Redis(connection_pool=pool)
