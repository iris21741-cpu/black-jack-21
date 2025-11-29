from enum import Enum


class GameStatus(Enum):
    NEW = 1
    BET = 2
    PLAYER_OPERATION = 3
    DEALER_OPERATION = 4
    STATEMENT = 5
    GAME_OVER = 6

    @classmethod
    def get(cls, value):
        """依數值取得對應 GameStatus，無效則回 None"""
        try:
            return GameStatus(value)
        except ValueError:
            return None

    @classmethod
    def operation_allow(cls, status):
        """回傳該狀態是否允許進行操作"""
        allowed_status = {
            cls.BET,
            cls.PLAYER_OPERATION,
            cls.STATEMENT
        }
        return status in allowed_status
