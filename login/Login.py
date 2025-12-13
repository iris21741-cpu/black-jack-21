from auth.JWTUtil import create_token
from dao.UserDao import get_by_email
from email2fa.CodeBuilder import generate_totp_code
from email2fa.EmailSender import send_code

#本地暫存用戶token資訊
user_token={}

def login(email:str,password:str):
    # 1.查email
    user=get_by_email(email)

    if user is None:
        return{
        "success":False,
        "message":"Email 不存在"
    }
    # 2.比對密碼（你的ORM是純文字密碼）
    if user.password !=password:
        return{
            "success":False,
            "message":"密碼錯誤"
        }

    # token = create_token(user.id, email)
    # r = redis_client()
    # cache = {
    #     "user": user.to_json_object(),
    #     "token": token
    # }
    # r.set("user:" + str(user.id), json.dumps(cache))
    # user_token.append(cache)

    # 建2FA驗證碼
    code = generate_totp_code(user.otp_secret)
    # 發送驗證碼到用戶信箱
    ok = send_code(user.email, code)
    if not ok :
        return {
            "success": False,
            "message": "驗證碼發送失敗",
            "user": user.to_json_object()
            # "token": token
        }
    else:
        # 3. 成功登入
        return {
            "success": True,
            "message": "登入成功，請至 email 收取驗證碼",
            "user": user.to_json_object()
            # "token": token
        }

def gen_token(user):
    """
    驗證成功產生 token
    :param user: 用戶資料
    :return: json格式的用戶資訊和token
    """
    token=create_token(user.id,user.email)
    # r=redis_client()
    cache={
        "user":user.to_json_object(),
        "token":token
    }
    #r.set("user:"+str(user.id),json.dumps(cache)

    #本地暫存用戶的token 資訊
    user_token[user.id]=cache

    return cache
