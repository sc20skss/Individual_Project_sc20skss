from round import Round
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

   


class Game:
    def __init__(self, winning_value):
        self.win = winning_value 

        # Initial values
        self.players = ["A1", "B1", "A2", "B2"]
        self.round = 1
        self.scores = [0, 0]
        self.bags = [0, 0]
        self.discarded_bags = [0, 0]

    # Enforce the 7-bag penalty
    def score_bags(self):
        for i in range(2):
            while (self.bags[i] >= 7):
                self.bags[i] -= 7
                self.discarded_bags[i] += 7
                self.scores[i] -= 100

    # Rotate order of players every round. (First player of a round is the first to bid and lead!)
    def rotate_order(self):
        first = self.players.pop(0)
        self.players.append(first)

    # Return the name of the winning team, or "" if there is no winner
    def winner(self):
        if (max(self.scores[0],self.scores[1]) >= self.win):
            if (self.scores[0] > self.scores[1]):
                return "A"
            elif (self.scores[1] > self.scores[0]):
                return "B"
            else:
                # Tie breakers
                if (self.bags[0] + self.discarded_bags[0] > self.bags[1] + self.discarded_bags[1]):
                    return "B"
                elif (self.bags[1] + self.discarded_bags[1] > self.bags[0] + self.discarded_bags[0]):
                    return "A"
        return ""

    # Return a formatted string containing info about the game
    def game_header(self):
        return f"[Game Score: (A) {self.scores[0]} vs. {self.scores[1]} (B) | Bags: (A) {self.bags[0]} vs. {self.bags[1]} (B) | Goal: {self.win}]"

    # Handle the execution/refereeing of a Spades game
    def run(self):
        game_over = False
        while (not game_over):
            # Run a round
            roundResult = Round(self.round, self.players, self.game_header())

            # Adjust instance variables as needed based on round results
            self.scores[0] += roundResult.scores[0]
            self.scores[1] += roundResult.scores[1]
            self.round += 1
            self.bags[0] += roundResult.bags[0]
            self.bags[1] += roundResult.bags[1]

            # Setup for next round
            self.score_bags()
            self.rotate_order()
            winner = self.winner()
            game_over = (len(self.winner()) != 0)

            if (not game_over):
                print("Here is the current status of your game:\n")
                print(f"\t{self.game_header()}\n")
                handle_input("Press any key to continue to the next round...")

        # End of game message
        handle_input(f"Congrats to Team {winner} on their victory! Here are the final results:\n\n"
                     f"\t{self.game_header()}\n\n"
                     "I hope everyone enjoyed the Spades! Press any key to end the game...")
