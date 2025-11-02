from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Integer,
    SmallInteger,
    DateTime,
    text,
    Index
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.mysql import DATETIME

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    __table_args__ = (
        {"comment": "用戶資訊"},  # 對應 TABLE COMMENT
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    full_name = Column(
        String(255, collation="utf8mb4_bin"),
        nullable=False,
        comment="用戶全名",
        index=True
    )
    email = Column(
        String(255, collation="utf8mb4_bin"),
        nullable=False,
        comment="email",
        index=True
    )
    gender = Column(
        SmallInteger,
        nullable=True,
        server_default=text("1"),
        comment="性別 1.男 2.女",
        index=True
    )
    status = Column(
        Integer,
        nullable=False,
        server_default=text("1"),
        comment="0.停用 1.啟用"
    )
    create_time = Column(
        DATETIME(fsp=3),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP(3)"),
        comment="創建時間",
        index=True
    )
    last_edit_time = Column(
        DATETIME(fsp=3),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3)"),
        comment="最後更新時間"
    )

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.full_name}', email='{self.email}')>"
