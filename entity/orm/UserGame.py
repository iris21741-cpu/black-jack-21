# entity/orm/UserGame.py
from sqlalchemy import (
    Column, BigInteger, SmallInteger, text
)
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class UserGame(Base):
    __tablename__ = "user_game"
    __table_args__ = {"comment": "21點遊戲"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    status = Column(SmallInteger, nullable=False, server_default=text("1"),
                    comment="NEW=1,BET=2,PLAYER_OPERATION=3,DEALER_OPERATION=4,STATEMENT=5,GAME_OVER=6")
    crete_time = Column(DATETIME(fsp=3), nullable=False, server_default=text("CURRENT_TIMESTAMP(3)"))
    last_edit_time = Column(DATETIME(fsp=3), nullable=False,
                            server_default=text("CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3)"))

    def __repr__(self):
        return f"<UserGame(id={self.id}, status={self.status})>"
