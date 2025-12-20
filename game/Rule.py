from dealer.Dealer import Dealer
from player.Player import Player
import logging


def result_statement(player: Player, dealer: Dealer):
    dealer_score = dealer.hand.value()
    player_score = player.hand.value()

    if len(player.hand.cards) == 2 and player_score == 21:
        logging.info("玩家勝利！")
        return 2
    if len(player.hand.cards) == 5 and player_score <= 21:
        logging.info("玩家勝利")
        return 2
    if player_score > 21:
        logging.info("莊家勝利")
        return -1
    if dealer_score > 21 or player_score > dealer_score:
        logging.info("玩家勝利")
        return 1
    elif player_score < dealer_score:
        logging.info("莊家勝利")
        return -1
    else:
        logging.info("平手")
        return 0
