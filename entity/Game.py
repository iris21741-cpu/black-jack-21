from dealer.Dealer import Dealer
from entity.Deck import Deck
from enums.GameStatus import GameStatus
from game.Rule import result_statement
from player.Player import Player


class Game:
    def __init__(self, _id, name):
        self.id = _id
        self.player = Player(name)
        self.dealer = Dealer()
        self.status = GameStatus.NEW
        self.deck = Deck()

    def renew(self):
        self.player.hand.clear()
        self.dealer.hand.clear()
        self.status = GameStatus.NEW

    def to_json_object(self):
        return {
            "id": self.id,
            "player": self.player.to_json_object(),
            "dealer": self.dealer.to_json_object(),
            "status": self.status.name,
            "bet": self.player.bet,
            "chips": self.player.chips,
            "move": self.player.get_move()
        }

    def deal_cards(self):
        # 發牌
        for _ in range(2):
            self.player.hand.add_card(self.deck.deal())
            self.dealer.hand.add_card(self.deck.deal())
        print(self.dealer.show_current_value())
        print(self.player.show_current_value())

    def player_next_move(self):
        self.player.next_move()

    def player_operation(self, opt):
        if opt == "h":
            self.player.hand.add_card(self.deck.deal())
            print(self.player.show_current_value())
            self.player.is_first_turn = False
            self.check_player_value()
            return True
        elif opt == "s":
            # 莊家操作
            self.dealer_operation()
            self.status = GameStatus.STATEMENT

            statement = result_statement(self.player, self.dealer)
            self.player.statement_bet(statement)
            self.game_is_over()
            return True
        elif opt == "d" and self.player.is_first_turn:  # 只允許第一回合雙倍
            if self.player.bet * 2 <= self.player.chips:
                self.player.bet *= 2

                self.player.hand.add_card(self.deck.deal())
                print(self.player.show_current_value())
                self.check_player_value()
                return True
            else:
                print("籌碼不足，不能雙倍！")
                return False
        elif self.status == GameStatus.STATEMENT:
            # 繼續遊戲
            if opt == "Y":
                self.renew()
                return True
            # 結束遊戲
            elif opt == "N":
                self.status = GameStatus.GAME_OVER
                return True
        return False

    def dealer_operation(self):
        while self.dealer.hand.value() < 17 or self.player.hand.value() > self.dealer.hand.value():
            self.dealer.hand.add_card(self.deck.deal())
            print("莊家要牌：", self.dealer.hand, "點數：", self.dealer.hand.value())

    def show_result(self):
        player_score = self.player.hand.value()
        dealer_score = self.dealer.hand.value()
        print("\n最終結果：")
        print(self.player.show_current_value())
        print(self.dealer.show_current_value())

        statement = result_statement(self.player, self.dealer)
        self.player.statement_bet(statement)

    def check_player_value(self):
        if self.player.hand.value() >= 21 :
            result = result_statement(self.player, self.dealer)
            self.player.statement_bet(result)
            ok = False
        else:
            ok = True

        if not ok:
            self.game_is_over()
        else:
            self.status = GameStatus.PLAYER_OPERATION
            self.player.next_move()

    def game_is_over(self):
        if self.player.chips <= 0:
            self.status = GameStatus.GAME_OVER
            self.player.move = "遊戲結束"
        else:
            self.status = GameStatus.STATEMENT
            self.player.move = "要繼續遊戲嗎？（Ｙ／Ｎ）"