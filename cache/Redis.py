from redis import ConnectionPool, Redis

def redis_client():
    pool = ConnectionPool(
        host='localhost',
        port=6379,
        password=None,
        decode_responses=True,
        max_connections=10
    )

    return Redis(connection_pool=pool)

if __name__ == '__main__':
    r = redis_client()
    user = r.get("user:11")
    print(user)