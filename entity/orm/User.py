import re

import pyotp
from sqlalchemy import (
    Column, BigInteger, String, Integer, UniqueConstraint, Index
)
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
from sqlalchemy.sql import func

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

    # 🔑 新增：用於儲存 Base32 密鑰的欄位
    # Base32 密鑰通常約 16 到 32 個字元長，String(50) 已經足夠安全。
    # 必須設置為 nullable=True，因為用戶可能尚未啟用 2FA。
    otp_secret = Column(
        String(50, collation="utf8mb4_bin"),
        nullable=True,
        default=pyotp.random_base32,  # <--- 關鍵修改：使用 pyotp 函式作為 default
        comment="兩步驟驗證 (TOTP) 的 Base32 密鑰"
    )

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

    # ✅ 驗證密碼規則 (保持不變)
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

    # ✅ 驗證 email 格式 (保持不變)
    @validates("email")
    def validate_email(self, key, address):
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        if not re.match(pattern, address):
            raise ValueError(f"Invalid email format: {address}")
        return address

    def __repr__(self):
        # 在 __repr__ 中加入 otp_secret 以便調試
        return f"<User(id={self.id}, full_name='{self.full_name}', email='{self.email}', otp_secret={self.otp_secret is not None})>"

    def to_json_object(self):
        # 不應該在 JSON 物件中傳回 otp_secret，因為這是敏感資訊
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "status": self.status,
            "gender": self.gender,
            # 可以新增一個欄位表示是否啟用 2FA
            "is_2fa_enabled": self.otp_secret is not None,
            "create_time": self.create_time.timestamp(),
            "last_edit_time": self.last_edit_time.timestamp()
        }