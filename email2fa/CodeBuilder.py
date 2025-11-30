import pyotp


def generate_totp_code(secret) -> str:
    """
    使用 TOTP 演算法，基於當前時間和 SECRET_KEY 產生一個 6 位數的驗證碼。
    這個代碼會每 60 秒更新一次。

    Returns:
        str: 產生的 6 位數 TOTP 驗證碼。
    """
    # 使用 TOTP_GENERATOR 產生當前時間的驗證碼
    totp_generator = pyotp.TOTP(secret, interval=60)
    otp_code = totp_generator.now()
    return otp_code


def verify(secret, code) -> bool:
    """
    檢核驗證碼
    Returns:
        bool: 是否驗證成功
    """
    try:
        totp_generator = pyotp.TOTP(secret, interval=60)
        return totp_generator.verify(code)
    except Exception as e:
        print(f"TOTP verify error {e}")
        return False
