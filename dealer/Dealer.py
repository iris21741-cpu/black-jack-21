from player.Player import Player


class Dealer(Player):
    def __init__(self):
        super().__init__(0, "莊家", chips=999999)
