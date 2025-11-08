from sqlalchemy import (
    Column, BigInteger, String, Integer, text, UniqueConstraint, Index
)
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
import re

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    __table_args__ = (
        UniqueConstraint("email", name="uk_email"),
        Index("idx_full_name", "full_name"),
        Index("idx_gender", "gender"),
        Index("idx_create_time", "create_time"),
        {
            "mysql_engine": "InnoDB",
            "mysql_charset": "utf8mb4",
            "mysql_collate": "utf8mb4_unicode_ci",
            "comment": "用戶資訊",
        },
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    full_name = Column(String(255, collation="utf8mb4_bin"), nullable=False, comment="用戶全名")
    email = Column(String(255, collation="utf8mb4_bin"), nullable=False, comment="email")
    gender = Column(Integer, default=1, comment="性別 1.男 2.女")
    password = Column(String(100, collation="utf8mb4_bin"), nullable=False, comment="用戶密碼")
    status = Column(Integer, nullable=False, default=1, comment="0.停用 1.啟用")

    create_time = Column(
        DATETIME(fsp=3),
        nullable=False,
        server_default=func.now(),
        comment="創建時間",
    )
    last_edit_time = Column(
        DATETIME(fsp=3),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment="最後更新時間",
    )

    # ✅ 驗證密碼規則
    @validates("password")
    def validate_password(self, key, password):
        """
        密碼需符合：
        1. 至少 8 位數
        2. 至少 1 個大寫字母
        3. 至少 1 個小寫字母
        4. 至少 1 個特殊符號（!@#$%^&*()-_+= 等）
        """
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,}$"
        if not re.match(pattern, password):
            raise ValueError(
                "Password must be at least 8 characters long, "
                "contain both uppercase and lowercase letters, "
                "and include at least one special symbol."
            )
        return password

    # ✅ 驗證 email 格式
    @validates("email")
    def validate_email(self, key, address):
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        if not re.match(pattern, address):
            raise ValueError(f"Invalid email format: {address}")
        return address

    def __repr__(self):
        return f"<User(id={self.id}, full_name='{self.full_name}', email='{self.email}', password='{self.password}', status={self.status})>"

    def to_json_object(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "status": self.status,
            "gender": self.gender,
            "create_time": self.create_time,
            "last_edit_time": self.last_edit_time
        }