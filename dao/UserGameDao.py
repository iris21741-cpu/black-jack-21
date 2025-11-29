from entity.orm.UserGame import UserGame
from mysql.Engine import SessionLocal

# 新增
with SessionLocal() as session:
    new_user_game = UserGame(status=1)
    session.add(new_user_game)
    session.commit()
    session.refresh(new_user_game)
    print("✅ 新增：", new_user_game)

# 查詢
with SessionLocal() as session:
    user_games = session.query(UserGame).filter(UserGame.status == 1).all()
    for u in user_games:
        print(u)
