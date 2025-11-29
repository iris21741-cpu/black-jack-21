from dealer.Dealer import Dealer
from player.Player import Player


def result_statement(player: Player, dealer: Dealer):
    dealer_score = dealer.hand.value()
    player_score = player.hand.value()

    if len(player.hand.cards) == 2 and player_score == 21:
        print("玩家勝利！")
        return 2
    if len(player.hand.cards) == 5 and player_score <= 21:
        print("玩家勝利")
        return 2
    if player_score > 21:
        print("莊家勝利")
        return -1
    if dealer_score > 21 or player_score > dealer_score:
        print("玩家勝利")
        return 1
    elif player_score < dealer_score:
        print("莊家勝利")
        return -1
    else:
        print("平手")
        return 0
