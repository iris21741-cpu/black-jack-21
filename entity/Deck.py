import random
from entity.Card import Card
class Deck:
    suits=['♠', '♥', '♦', '♣']
    ranks=['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    def __init__(self):
        self.cards=None
        self.new_cards()

    def new_cards(self):
        self.cards= [Card(r,s)for s in self.suits for r in self.ranks]
        random.shuffle(self.cards)

    def deal(self):
        if len(self.cards)==0:
            self.new_cards()
        return self.cards.pop()

        