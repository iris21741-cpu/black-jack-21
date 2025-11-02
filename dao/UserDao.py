from mysql.Engine import SessionLocal
from entity.orm.User import User

# 新增
with SessionLocal() as session:
    new_user = User(full_name="王小明", email="ming@example.com", gender=1)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    print("✅ 新增：", new_user)

# 查詢
with SessionLocal() as session:
    users = session.query(User).filter(User.status == 1).all()
    for u in users:
        print(u)
