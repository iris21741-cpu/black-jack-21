from redis import ConnectionPool, Redis
"""這段程式碼採用了將連線管理和命令執行分離的設計：
連線池 (ConnectionPool)：負責處理網路連線的建立、維護和資源限制。它的存在使得應用程式可以重用已建立的連線，極大地提高了效能（避免了頻繁的 TCP 握手開銷）。
客戶端 (Redis)：負責提供所有 Redis 命令的 Python 介面。它將連線的細節委託給 ConnectionPool 處理，自己專注於發送和接收命令。"""

def redis_client():
    pool = ConnectionPool(
        host='localhost',
        port=6379, # Redis 預設 Port（可改）
        password=None,
        decode_responses=True,  # 自動把 bytes 轉成字串
        max_connections=10
    )

    return Redis(connection_pool=pool)
