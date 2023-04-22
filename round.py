from contract import Contract
from ai_agent import Model, MCTSModel
import random
import getpass
from card import Card


import os

YORN = 2
QUIT = 'q'
RULES = 'r'
CONTINUE = 0

DIVIDER = '——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————\n'
HEADER = ("+------------------------+\n" 
          "| ♠♠♠♠♠ SPADE GAME ♠♠♠♠♠ |\n"
          "+------------------------+\n")
# Handle quitting mid-game
def kill_game(msg, type):
    
    response = None
    while (True):
        response = input("Quit game? (y/n)\n>>>").upper()
        if (response == 'Y'):
            quit()
        elif (response == 'N'):

            # "Go back" to the original prompt (and hope the user doesn't descend much further into the call stack)
            return handle_input(msg, type)




def handle_input(msg, type=(CONTINUE)):
    response = input(msg + "\n>>>")
    if (response == QUIT):
        return kill_game(msg, type)
    else:
        if (type == YORN):
            response = response.upper()
            if (response == 'NO' or response == 'N'):
                return False
            elif (response == 'YES' or response == 'Y'):
                return True
            else:
                return handle_input(msg, type)

        return response

class Round:
    def __init__(self, num, players, game_header):
        self.num = num
        self.players = players
        self.game_state = game_header 
        self.scores = [0, 0]
        self.bags = [0, 0]
        self.winnings = {'A1': 0, 'B1': 0, 'A2': 0, 'B2': 0}
        self.contracts = [Contract(), Contract()]
        self.hands = {}
        self.spade_in_play = False 

        self.played_cards = { 'A1' : [], 'B1' : [], 'A2' : [], 'B2' : []}
        self.ai_agent_min_max : Model = None 
        self.ai_agent_mcts : MCTSModel = None

        # Run the round
        self.run()

    def deal_cards(self):
        deck = [Card(i) for i  in range(52)]
        for i in range(random.randint(1,8)): random.shuffle(deck)
        for i, player in enumerate(self.players):
            hand = [deck[c] for c in range(i,i+4*12+1,4)]
            hand.sort(key=(lambda k: k.id))

            self.hands[player] = hand

  
    def print_hand(self, hand, selection=[]):
        buffer = []
     
        for i, card in enumerate(hand):
            data = card.viz()
            # Add an extra row to the string to denote user input selector
            if (len(selection) > 0):
                if (i not in selection):
                    selection_string = f"   XXX   "
                elif (i < 10):
                    selection_string = f"   [{i}]   "
                else:
                    selection_string = f"   [{i}]  "
                data.append(selection_string)

            buffer.append(data)

        # Print cards line by line
        if (len(buffer) > 0):
            for i in range(len(buffer[0])):
                line = []
                last_suite = hand[0].suiteID
                for j, card in enumerate(buffer):
                 
                    if (hand[j].suiteID != last_suite):
                        line.append('   ')
                        last_suite = hand[j].suiteID
                 
                    line.append(card[i])
         
                print(''.join(line))
        print()

    def print_table(self, table, ordering):
        print("On The Table:")
        buffer = []
      
        for i, card in enumerate(table):
            data = card.viz()
            buffer.append(data)

        while (len(buffer) < 4):
            ghost_card = [ "┌ ─ ─ ─ ┐",
                           "         ",
                           "│       │",
                           "         ",
                           "└ ─ ─ ─ ┘"]
            buffer.append(ghost_card)

      
        for i, card_str in enumerate(buffer):
            player = ordering[i]
            player_string = f"  {i + 1}: {player}  "
            card_str.append(player_string)

        # Print cards line by line
        if (len(buffer) > 0):
            for i in range(len(buffer[0])):
                line = []
                for j, card in enumerate(buffer):
                    line.append(' ')
                    line.append(card[i])
                # Flush out results
                print(''.join(line))
        print()

    # Print the status of the game at the top of the screen
    def print_header(self):
        teamA = f"{self.contracts[0].to_string(self.winnings['A1'], self.winnings['A2'])}"
        teamB = f"{self.contracts[1].to_string(self.winnings['B1'], self.winnings['B2'])}"
        left = f"Round #{self.num} | Bids: (A) {teamA} vs. {teamB} (B)"
        right = self.game_state

        # Justify columns to edges
        padding = []
        for i in range(232 - len(left) - len(right)):
            padding.append(' ')
        padding = ''.join(padding)
        print(left + padding + right)
        # Print a row of dashes to underline header
        print(DIVIDER)

    def get_bet(self,p_no):
        if(p_no==-1):
            msg = "Enter how many hands you can win : "
            while (True):
                bid = handle_input(msg)
                try:
                    bid = int(bid)
                    if ((bid < 0) or (bid > 13)):
                        print("Your bid must be range from 0 to 13 !!!")
                    else:
                        return bid
                except:
                    print("Enter an integer!")
        else:
            bid=random.randint(1,4)
            return bid


    def bidding(self):
        for i, player in enumerate(self.players):
           
            
            if(i==-1):
                self.print_header()
                blind_msg = ("Would you like to view your cards? Answering no means "
                                "you will be bidding blind. (y/n)")
                not_blind = handle_input(blind_msg, YORN)
                # Show cards unless blind
                if (not_blind):
                    self.print_hand(self.hands[player])
                else:
                    print("Yikes! Good luck bidding blind!")

       
            bid_result = self.get_bet(i)
            not_blind = True
           
            team = player[0]
            number = int(player[1])
            if (team == "A"):
                self.contracts[0].add_bid(number, bid_result, not not_blind)
            else:
                self.contracts[1].add_bid(number, bid_result, not not_blind)

            # Tell the user what to do next
            if (i ==0):
                handle_input("Bid accepted!  Press any key to continue....")
            elif (i==1):
                print('Player 2 done bidding : ',bid_result)
            elif (i==2):
                print('Player 3 done bidding : ',bid_result)
            elif (i==3):
                print('Player 4 done bidding : ',bid_result)
            else:
                self.print_header()
                handle_input("All bids are made! press any key to begin play....")
        bids = {'A1' : self.contracts[0].bids[0], 'A2' : self.contracts[0].bids[1], 
                        'B1' : self.contracts[1].bids[0], 'B2' : self.contracts[1].bids[1] }
        self.ai_agent_min_max = Model(bids)
        self.ai_agent_mcts = MCTSModel(bids)

    def play_trick(self, ordering):
        table = []      
        lead_suite = -1 
        self.print_header()
        self.print_table(table, ordering)
        self.spade_in_play = False

        human = 'None'
        min_max_team = ['A1', 'A2']

        for i, player in enumerate(ordering):
            
            player_i = i
            selectable = []
            for i, card in enumerate(self.hands[player]):
                if (lead_suite == -1 and self.spade_in_play):
                    selectable.append(i) 
                elif (lead_suite == -1 and card.suiteID != 3):
                    selectable.append(i) 
                elif (lead_suite == card.suiteID):
                    selectable.append(i) 
            if (len(selectable) == 0):
                selectable = [i for i in range(len(self.hands[player]))] 
            else:
                for i, card in enumerate(self.hands[player]):
                    if (card.suiteID == 3 and self.spade_in_play):
                        selectable.append(i) # Once a spade has been played, they may always be played

         
            print("In Your Hand:")
            print(selectable)

            self.print_hand(self.hands[player], selectable)

            if player == human:
                # getting the index of card to be played
                while (True):
                    result = handle_input("Enter the number under the card which you want to play")
                    try:
                        result = int(result)
                        if (result not in selectable):
                            print("ERROR !!! Not a valid number!")
                        else:
                            break
                    except:
                        print("ERROR !!! Not a valid number!")
            elif player in min_max_team:
                print("Min max team")
                print(ordering)
                result = self.ai_agent_min_max.run(self.played_cards, self.hands[player], selectable, ordering, player_i, table)
            else:
                print("Monte Cralo Tree Search Team")
                print(ordering)
                self.ai_agent_mcts.set_hands(self.hands)
                result = self.ai_agent_mcts.run(self.played_cards, self.hands[player], selectable, ordering, player_i, table)

    
            self.played_cards[player].append(self.hands[player][result])

            played_card = self.hands[player].pop(result)
            table.append(played_card)

           
            if (lead_suite == -1):
                lead_suite = played_card.suiteID
            if (played_card.suiteID == 3):
                # lead_suite = 3
                self.spade_in_play = True

            self.print_header()
            self.print_table(table, ordering)
            

        # Determining the winner 
        best_card = table[0]
        winner = ordering[0]
        if self.spade_in_play: lead_suite = 3

        for i, card in enumerate(table):
            if (card.suiteID == lead_suite):
                if ((card.orderID > best_card.orderID) or (best_card.suiteID != lead_suite)):
                    best_card = card
                    winner = ordering[i]

        return winner, best_card

    #trick played by the players

    def play_round(self):
        ordering = [p for p in self.players]
        lead_player = ordering[0]

        
        for i in range(13):
            lead_player, best_card = self.play_trick(ordering)
            self.winnings[lead_player] += 1
            msg = (f"Player {lead_player} won the hand with {best_card.order}{best_card.suite}! Press any key to continue...")
            handle_input(msg)

            # rotating untill the winner comes first

            while (lead_player != ordering[0]):
                ordering.append(ordering.pop(0))

 
    def score(self):
        self.print_header()
        print("The round is over!\n")
        print("Scores are written below :")

        # evaluating each bidding/contract
        scoreA, bagA = self.contracts[0].eval(self.winnings['A1'], self.winnings['A2'])
        scoreB, bagB = self.contracts[1].eval(self.winnings['B1'], self.winnings['B2'])

        self.scores = [scoreA, scoreB]
        self.bags = [bagA, bagB]

        print("Team A:")
        print(f"\tContract:\t{self.contracts[0].to_string(self.winnings['A1'], self.winnings['A2'])}")
        print(f"\tScore:\t\t{scoreA}")
        print(f"\tBags:\t\t{bagA}")
        print()
        print("Team B:")
        print(f"\tContract:\t{self.contracts[1].to_string(self.winnings['B1'], self.winnings['B2'])}")
        print(f"\tScore:\t\t{scoreB}")
        print(f"\tBags:\t\t{bagB}")
        print()
        handle_input("Press any key to end the round...")

    # the spade game 
    def run(self):
        self.deal_cards()
        self.bidding()
        self.play_round()
        self.score()
