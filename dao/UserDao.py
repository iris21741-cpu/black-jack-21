from mysql.Engine import SessionLocal
from entity.orm.User import User
from sqlalchemy.exc import SQLAlchemyError

def create_user(new_user: User):
    """建立新用戶紀錄"""
    try:
        with SessionLocal() as session:
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            print("✅ 新增成功：", new_user)
            return new_user
    except SQLAlchemyError as e:
        print("❌ 新增失敗，錯誤原因：", str(e))
        # 若出錯記得 rollback，避免 session 卡死
        try:
            session.rollback()
        except Exception:
            pass
        raise
