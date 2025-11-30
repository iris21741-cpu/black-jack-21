from datetime import datetime, timedelta, UTC

import jwt

SECRET_KEY = "iris21741"  # 🔥 請放你自己的秘密字串
ALGORITHM = "HS256"
EXPIRE_MINUTES = 60 * 24  # Token 有效時間（24 小時）


def create_token(user_id: int, email: str):
    expire_time = datetime.now(UTC) + timedelta(minutes=EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),  # 使用者 ID 用來識別使用者
        "email": email,
        "exp": expire_time  # 過期時間
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    """
    驗證 JWT Token
    1. 簽章正確
    2. 未過期
    3. 回傳 payload
    """
    try:
        # 解碼 JWT Token，驗證簽名和有效期限
        # payload 包含了您在簽發 Token 時放入的用戶資訊
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return data
    except jwt.ExpiredSignatureError:
        return {
            'message': 'Token has expired!',
            'code': 40102
        }
    except jwt.InvalidSignatureError:
        return {
            'message': 'Token signature is invalid!',
            'code': 40103
        }
    except Exception as e:
        # 處理其他如格式錯誤等問題
        return {
            'message': f'Token is invalid or malformed: {e}',
            'code': 40104
        }


if __name__ == '__main__':
    # 1. 生產 token
    token_str = create_token(1, "123@gmail.com")
    print(token_str)
    # 2. 驗證 token
    payload = verify_token(token_str)
    print(payload)
