# 階段 1：構建階段 (Build Stage)
FROM python:3.11-slim AS builder

# 安裝必要的系統依賴 (如果你的包需要編譯，例如 psycogp2 或 numpy)
# RUN apt-get update && apt-get install -y --no-install-recommends \
# build-essential \
# gcc \
# && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 將 requirements.txt 複製到構建鏡像
COPY requirements.txt .

# 安裝依賴到虛擬環境或其他目錄
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 階段 2：運行階段 (Final Stage)
# 使用更小的運行時基礎鏡像
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /usr/src/app

# 從 'builder' 階段複製已安裝的 Python 依賴
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
# 複製應用程式代碼
COPY . .

# 暴露端口 port
EXPOSE 5000
ENV ENV_FILE=.env.prod

# 定義容器啟動時運行的命令
CMD ["python", "main.py"]