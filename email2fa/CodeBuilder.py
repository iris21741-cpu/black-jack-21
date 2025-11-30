import pyotp
import time # 用來模擬時間流逝

# ----------------------------------------------------------------------
# 注意：在真實應用中，每個用戶應該有一個獨特的密鑰 (SECRET_KEY)。
# 此處為了範例方便，使用了一個靜態密鑰。
# SECRET_KEY 必須是 Base32 編碼的字串。
# ----------------------------------------------------------------------
# 範例密鑰：請務必將此替換為安全且隨機生成的密鑰！
SECRET_KEY = "26UBSCADRYPGCFRI4UQSRGLN7XC67MH2"

# 創建一個 TOTP 物件，並將步進 (interval) 設置為 60 秒
# 這表示每 60 秒會產生一個新的驗證碼
TOTP_GENERATOR = pyotp.TOTP(SECRET_KEY, interval=60)

def generate_totp_code() -> str:
    """
    使用 TOTP 演算法，基於當前時間和 SECRET_KEY 產生一個 6 位數的驗證碼。
    這個代碼會每 60 秒更新一次。

    Returns:
        str: 產生的 6 位數 TOTP 驗證碼。
    """
    # 使用 TOTP_GENERATOR 產生當前時間的驗證碼
    otp_code = TOTP_GENERATOR.now()
    return otp_code

if __name__ == '__main__':
    secret_key = pyotp.random_base32()
    print(secret_key)