# entity/orm/GamePlayer.py
from sqlalchemy import (
    Column, BigInteger, Integer, SmallInteger, String,
    text
)
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class GamePlayer(Base):
    __tablename__ = "game_player"
    __table_args__ = {"comment": "遊戲玩家"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, comment="用戶id")
    game_id = Column(BigInteger, nullable=False, comment="遊戲id")
    chips = Column(Integer, nullable=False, server_default=text("0"), comment="金額")
    bet = Column(Integer, nullable=False, server_default=text("0"), comment="下注金額")
    is_fist_turn = Column(SmallInteger, nullable=False, server_default=text("1"), comment="False=0,True=1")
    type = Column(SmallInteger, nullable=False, server_default=text("1"), comment="1. 玩家, 2. 莊家")
    user_move = Column(String(255, collation="utf8mb4_unicode_ci"), nullable=True, comment="玩家操作")
    crete_time = Column(DATETIME(fsp=3), nullable=False, server_default=text("CURRENT_TIMESTAMP(3)"))
    last_edit_time = Column(DATETIME(fsp=3), nullable=False,
                            server_default=text("CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3)"))

    def __repr__(self):
        return f"<GamePlayer(id={self.id}, user_id={self.user_id}, game_id={self.game_id}, chips={self.chips})>"
