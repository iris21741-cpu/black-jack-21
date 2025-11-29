from dao.UserDao import create_user
from entity.orm.User import User
from enums.UserStatus import UserStatus


def register(full_name, email, gender, password):
    new_user = User(full_name=full_name, email=email, gender=gender, password=password, status=UserStatus.NEW)
    create_user(new_user)
    return new_user
