from entity.Hand import Hand


class Player:
    def __init__(self, name, chips=1000):
        self.name = name
        self.hand = Hand()
        self.chips = chips
        self.bet = 0
        self.is_first_turn = True
        self.move = ""

    def show_current_value(self):
        return f"[{self.name}]手牌:{self.hand}點數：{self.hand.value()}"

    def place_bet(self):
        while True:
            try:
                bet = int(input(f"{self.name}請下注 (目前籌碼{self.chips}):"))
                if 1 <= bet <= self.chips:
                    self.bet = bet
                    break
                else:
                    print("下注金額無效，請重新輸入整數金額")

            except ValueError:
                print("請輸入數字")

    def statement_bet(self, statement):
        result = self.chips + self.bet * statement
        print(f"籌碼{self.chips}->{result}")
        self.chips = result

    def next_move(self):
        if self.is_first_turn:
            self.move = "要牌（h）/ 停牌（s) / 雙倍（d):"
        else:
            self.move = "要牌（h）/ 停牌（s）:"

    def get_move(self):
        return self.move
