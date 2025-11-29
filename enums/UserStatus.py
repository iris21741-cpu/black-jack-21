from enum import IntEnum


class UserStatus(IntEnum):
    NEW = 1

    @classmethod
    def get(cls, value):
        """依數值取得對應 UserStatus，無效則回 None"""
        try:
            return UserStatus(value)
        except ValueError:
            return None

    # @classmethod
    # def operation_allow(cls, status):
    #     """回傳該狀態是否允許進行操作"""
    #     allowed_status = {
    #         cls.NEW,
    #     }
    #     return status in allowed_status
