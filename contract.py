class Contract:
    def __init__(self):
        self.sum = 0
        self.bids = [0, 0]
        self.teammate1_bid_val = 0
        self.teammate2_bid_val = 0
        self.bidStrings = ["YTB", "YTB"]
        self.blinds = [False, False]

 
    def add_bid(self, number, bid, blind):
        self.sum += bid
        self.bids[number - 1],self.blinds[number - 1],self.bidStrings[number - 1] = bid, blind, str(bid)
        if (blind):
            self.bidStrings[number - 1] += 'b'

#Changed the evaluation to suit the testing: (No lose of points)
    def eval(self, win1, win2):
        score = 0
        bags = 0
        wins = [win1, win2]

        overflow = (win1 + win2) - self.sum
        for i, bid in enumerate(self.bids):
            if (bid == 0):
                if (overflow > 0 or (wins[i] != 0)):
                    if (self.blinds[i]):
                        pass
                else:
                    score += 100
                    if (self.blinds[i]):
                        score += 100
            elif (overflow >= 0):
                if (self.blinds[i]):
                    if (wins[i] - bid < 0):
                        pass
                    else:
                        score += 100
                else:
                    score += bid * 10
            else:
                if (self.blinds[i]):
                    pass
                else:
                    # no points for not achieving bid
                    score += 0

        if (overflow > 0):
            for i, bid in enumerate(self.bids):
                diff = wins[i] - bid
                if (diff > 0):
                    score += diff
                    if (not self.blinds[i]):
                        bags += diff
        return score, bags

   
    def to_string(self, win1, win2):
        return (f"{{{win1}/{self.bidStrings[0]}, {win2}/{self.bidStrings[1]}}}")

# Sources https://github.com/ReillyBova/spades/blob/master/contract.py
