class Card:
    def __init__(self, card_id):
        self.id = card_id

        # Identify Suite
        if (card_id < 13):
            self.suite = '♦'
            self.suiteID = 0
        elif (card_id < 26):
            self.suite = '♣'
            self.suiteID = 1
        elif (card_id < 39):
            self.suite = '♥'
            self.suiteID = 2
        else:
            self.suite = '♠'
            self.suiteID = 3

        # Identify Order
        rem = (card_id % 13) + 2
        self.orderID = rem
        if (rem <= 10):
            self.order = str(rem)
        elif (rem == 11):
            self.order = 'J'
        elif (rem == 12):
            self.order = 'Q'
        elif (rem == 13):
            self.order = 'K'
        elif (rem == 14):
            self.order = 'A'

#Original Work is the values of the card and suit

    def getValue(self):
        val = 0
        if self.suite == '♠': val = 20
        if self.order == 'A': val += 14
        elif self.order == 'J': val += 11
        elif self.order == 'Q': val += 12
        elif self.order == 'K': val += 13
        else: val += int(self.order)
        return val

    def __str__(self) -> str:
        return f"[{self.order} | {self.suite}]"
    # For representation (multi-line, so returning array makes it easier to arrange cards horizontally later)
    def viz(self):
        symbol = self.suite
        ord = self.order[0]
        if (len(self.order) == 2):
            pad = self.order[1]
        else:
            pad = ' '

        # Style influenced by https://codereview.stackexchange.com/questions/82103/ascii-fication-of-playing-cards
        return [ "┌───────┐",
                f"│{ord}{pad}     │",
                f"│   {symbol}   │",
                f"│     {ord}{pad}│",
                 "└───────┘"]
#Source and adapted from https://github.com/ReillyBova/spades/blob/master/card.py
#
