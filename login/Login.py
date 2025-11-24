import json

from auth.JWTUtil import create_token
from dao.UserDao import get_by_email

user_token=[]
def login(email: str, password: str):
    # 1. 查 email
    user = get_by_email(email)

    if user is None:
        return {
            "success": False,
            "message": "Email 不存在"
        }

    # 2. 比對密碼（你的 ORM 是純文字密碼）
    if user.password != password:
        return {
            "success": False,
            "message": "密碼錯誤"
        }

    token = create_token(user.id, email)
    # r = redis_client()
    cache = {
        "user": user.to_json_object(),
        "token": token
    }
    # r.set("user:" + str(user.id), json.dumps(cache))
    user_token.append(cache)

    # 3. 成功登入
    return {
        "success": True,
        "message": "登入成功",
        "user": user.to_json_object(),
        "token": token
    }