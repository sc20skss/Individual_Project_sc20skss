import random
from card import Card
import numpy as np
from MonteCarloState import MCState

# get lowest playable card 
def get_lowest_value_card(hand, selectable):
    lowest_pos = -1
    value = 10000
    for i in selectable:
        if hand[i].getValue() < value:
            value = hand[i].getValue()
            lowest_pos = i
    assert(lowest_pos != -1)
    return lowest_pos


class Model:
    def __init__(self, bids) -> None:
        self.bids = bids
        self.players = ['A1', 'B1', 'A2', 'B2']
        self.cur_player = None
        self.teammate = None
        self.table = []

    def run(self, played_cards, my_cards, selectable, ordering, pos, table) -> int:
        self.cur_player = ordering[pos]
        self.teammate = None
        self.table = table

        if self.cur_player == 'A1': self.teammate = 'A2'
        elif self.cur_player == 'A2': self.teammate = 'A1'
        elif self.cur_player == 'B2': self.teammate = 'B1'
        elif self.cur_player == 'B1': self.teammate = 'B2'

        # apply some algo here
        MAX_DEPTH = 4 - pos

        result = self.minimax_algo(pos, my_cards, played_cards, selectable)
        if pos >= 2: 
            if my_cards[result].getValue() < table[pos-2].getValue():
                return get_lowest_value_card(my_cards, selectable)
        return result
    
    def getWinningCard(self):
        # print("Winning....")
        vals = []
        for card in self.table: vals.append(card.getValue())
        win_pos = np.argmax(vals)
        # print("win_pos: ", win_pos)
        return win_pos, self.table[win_pos]

    def minimax_algo(self, pos, my_cards, played_cards, selectable): 
        if pos < 2:
            if pos == 0: return self._getMin(my_cards, selectable)
            else: return self._getMax(my_cards, selectable)    
        else:
            win_id, winner_card = self.getWinningCard()
            if win_id + 2 == pos: return self._getMin(my_cards, selectable)
        return self._getMax(my_cards, selectable)

    def _getMax(self, my_cards, selectable):
        vals = []
        for i, card in enumerate(my_cards):
            if i in selectable:
                vals.append(card.getValue())
            else:
                vals.append(-1)
        return np.argmax(vals)

    def _getMin(self, my_cards, selectable):
        vals = []
        for i, card in enumerate(my_cards):
            if i in selectable:
                vals.append(card.getValue())
            else:
                vals.append(-1)
        return np.argmax(vals)


class MCTSModel():
    def __init__(self, bids) -> None:
        self.bids = bids
        self.players = ['A1', 'B1', 'A2', 'B2']
        self.cur_player = None
        self.teammate = None
        self.table = []
        self.round_hands = {}

    def UCBValue(self, state : MCState):
        parent = state.GetParent()
        C = 10
        return (state.wins/(state.visitCount) + C *(np.sqrt(np.log(parent.visitCount)/(state.visitCount))))

    def getBestChild(self, CardsQueue):
        BestChild = None
        Bestscore = 0
        for state in CardsQueue:
            if Bestscore < self.UCBValue(state) and len(state.chidren)==0:
                BestChild = state
                Bestscore = self.CalcUCTVal(state)
        return BestChild

    def getWinningCard(self, table):
        # print("Winning....")
        vals = []
        for card in table: vals.append(card.getValue())
        win_pos = np.argmax(vals)
        # print("win_pos: ", win_pos)
        return win_pos, table[win_pos]

    def set_hands(self, hands):
        self.round_hands = hands

    def run(self, played_cards, my_cards, selectable, ordering, pos, table) -> int:
        
        self.cur_player = ordering[pos]
        self.teammate = None
        self.table = table

        if self.cur_player == 'A1': self.teammate = 'A2'
        elif self.cur_player == 'A2': self.teammate = 'A1'
        elif self.cur_player == 'B2': self.teammate = 'B1'
        elif self.cur_player == 'B1': self.teammate = 'B2'

        result = self.MonteCarlo(pos, my_cards, played_cards, selectable)
        if pos >= 2: 
            if my_cards[result].getValue() < table[pos-2].getValue():
                return get_lowest_value_card(my_cards, selectable)
        return result

    def MonteCarlo(self, pos, my_cards, played_cards, selectable):
        CardsQueue = []
        for sel in selectable:
            CardsQueue.append(MCState(my_cards[sel]))
        Max_Iter = 1

        for i in range(Max_Iter):
            #Selection
            scores = []
            for state in CardsQueue:
                scores.append(self.UCBValue(state))
            
            #Expansion
            mx_val = max(scores)
            idxs = scores == mx_val

            # print(f"mx_val : {mx_val}, idx: {idxs}")

            res = -1
            wins = []
            goood_moves = []
            #Simulation
            for i, can in enumerate(idxs):
                try:
                    if not can: continue
                    opp_cards = []
                    team = []
                    for plyr in ['A1', 'B1', 'A2', 'B2']:
                        if plyr in self.teammate: 
                            for cc in self.round_hands[plyr]: team.append(cc)
                        else:
                            for cc in self.round_hands[plyr]: opp_cards.append(cc)

                    temp_table = [cc for cc in self.table]
                    assert(len(temp_table) < 4)
                    temp_table.append(CardsQueue[i].card_id)
                    cur_pos = len(temp_table)
                    agent_pos = cur_pos - 1
                    while len(temp_table) < 4:
                        cur_pos = len(temp_table)
                        if cur_pos%2 == 1:
                            temp_table.append(np.random.choice(team))
                        else:
                            temp_table.append(np.random.choice(opp_cards))

                    win_pos, win_card = self.getWinningCard(temp_table)
                    if win_pos == agent_pos:
                        wins.append(1)
                        goood_moves.append(CardsQueue[i].card_id)
                    else:
                        wins.append(0)
                except Exception as e:
                    res = -1
                    return np.random.choice(selectable)

            #Backpropagation
            for i, state in enumerate(CardsQueue):
                state.AddSimulations()
                if wins[i] == 1:
                    state.AddWins()
                
        # print(f"--> {len(goood_moves)}")
        if len(goood_moves) > 0:
            # print("<<<<<<< >>>>>>>>>>> ----------- <<>>> Selecting good move")
            for sel in selectable:
                if my_cards[sel] == goood_moves[0]:
                    return sel
        else:
            res = np.random.choice(selectable)
        assert(res != -1)
        return res


class MCState():
    def __init__(self, cid):
        self.card_id = cid
        self.chidren = []
        self.parent = self
        self.simulations = 1
        self.wins = 0
        self.visitCount = 1
    def Addchild(self, childstate):
        self.chidren.append(childstate)
    def GetChildren(self, parent):
        return self.chidren
    def SetParent(self, parent):
        self.parent = parent
    def GetParent(self, state = None):
        if state == None: return self.parent
        return state.parent
    def AddSimulations(self, num = 1):
        self.simulations += num
    def GetSimulations(self):
        return self.simulations
    def AddWins(self, num = 1):
        self.wins += num
    def GetWins(self):
        return self.wins
    def AddVisitCounts(self):
        self.visitCount += 1
    def GetVisitCounts(self):
        return self.visitCount

