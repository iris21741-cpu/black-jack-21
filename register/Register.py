from dao.UserDao import create_user, get_by_email
from entity.orm.User import User
from enums.UserStatus import UserStatus


def checkRegister(email):
    user = get_by_email(email)
    if user is None:
        return True
    else:
        return False

def register(full_name,email,gender,password):
    new_user=User(full_name=full_name,email=email,gender=gender,password=password)
    create_user(new_user)
    return new_user
