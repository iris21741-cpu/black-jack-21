import logging

from entity.orm.GamePlayer import GamePlayer
from mysql.Engine import SessionLocal

# 新增
with SessionLocal() as session:
    new_game_player = GamePlayer(user_id=1, game_id=1, chips=0, bet=0, is_first_turn=1,
                                 type=1, user_move=None)
    session.add(new_game_player)
    session.commit()
    session.refresh(new_game_player)
    logging.info("✅ 新增：", new_game_player)

# 查詢
with SessionLocal() as session:
    game_players = session.query(GamePlayer).filter(GamePlayer.game_id == 1).all()
    for g in game_players:
        logging.info(g)
