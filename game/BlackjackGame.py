from dealer.Dealer import Dealer
from entity.Deck import Deck
from entity.Hand import Hand
from game.Rule import result_statement
from player.Player import Player
# 舊的遊戲
class BlackjackGame:
    def __init__(self):
        self.deck=Deck()
        self.player=Player("玩家")
        self.dealer=Dealer()

    def play_round(self):
        # 清空手牌
        self.player.hand=Hand()
        self.dealer.hand=Hand()

        # 玩家下注
        self.player.place_bet()
        # 發牌
        for _ in range(2):
            self.player.hand.add_card(self.deck.deal())
            self.dealer.hand.add_card(self.deck.deal())
        print(self.dealer.show_current_value())
        print(self.player.show_current_value())
        # 玩家回合
        first_turn=True
        while self.player.hand.value()<21 and len(self.player.hand.cards) < 5:
            if first_turn:
                move=input("要牌（h）/ 停牌（s) / 雙倍（d):".lower())
            else:
                move=input("要牌（h）/ 停牌（s）:").lower()
            if move=="h":
                 self.player.hand.add_card(self.deck.deal())
                 print(self.player.show_current_value())
                 first_turn=False
            elif move =="s":
                 break
            elif move =="d" and first_turn:    #只允許第一回合雙倍
                if self.player.bet *2<=self.player.chips:
                    self.player.bet*=2
                    print(f"您選擇雙倍下注！新賭局：{self.player.bet}")
                    self.player.hand.add_card(self.deck.deal())
                    print(self.player.show_current_value())
                    break       # 抽完一張後必須停牌
                else:
                    print("籌碼不足，不能雙倍！")
                    continue

            else:
                print("輸入錯誤，請重新選擇")
        if self.player.hand.value()>21:
                print("玩家玩爆了！莊家勝利。"+ self.player.show_current_value())
        else:
            # 莊家回合
         print("\n莊家手牌：",self.dealer.hand,"點數：",self.dealer.hand.value())
         while self.dealer.hand.value()<17 or self.player.hand.value()>self.dealer.hand.value():
             self.dealer.hand.add_card(self.deck.deal())
             print("莊家要牌：",self.dealer.hand,"點數：",self.dealer.hand.value())

         # 判斷勝負
        self.show_result()

    def show_result(self):
        player_score=self.player.hand.value()
        dealer_score=self.dealer.hand.value()
        print("\n最終結果：")
        print(self.player.show_current_value())
        print(self.dealer.show_current_value())

        statement=result_statement(self.player,self.dealer)
        self.player.statement_bet(statement)

    def play(self):
        print("歡迎來到21點遊戲！")
        self.player.name=input("請輸入名稱： ")
        while self.player.chips>0:
            self.play_round()
            print(f"剩餘籌碼：{self.player.chips}")
            if self.player.chips >0:
                again=input("要繼續遊戲嗎？（Ｙ／Ｎ）").lower()
                if again.lower()=="y":
                    continue
                print("遊戲結束，謝謝遊玩")
                return








