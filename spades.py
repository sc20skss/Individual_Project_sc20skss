import os
from game import Game


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


def welcome():
    os.system("clear")
    print(HEADER)
    hello_msg = ("Welcome to Spades Game! Team A (Using Min-Max Algorithm) and Team B (Using Monte Carle Algorithm ) will be playing here! \nTo Quit: you may enter 'q' to quit and To read rules: 'r' to read the rules.\n\n"
                 "Note: Press 'Enter' key after typing your inputs in order to submit it to the game ")
    handle_input(hello_msg)

# Handles game setup and invokes play
def run_game():
    # Select the winning value
    winning_value = 1
    mode = 0 # 0: viewing (default), 1,3: playing in minimax team, 2,4: playing in monte-carlo team
    print("Select Game  mode:\n\t0: viewing\n\t1: playing in minimax team as A1\n\t2: playing in monte-carlo team as B1\n\t3: playing in minimax team as A2\n\t4: playing in monte-carlo team as B2")
    while True:
        try:
            choice = int(input("Enter mode number (0/1/2/3/4): "))
            if choice not in [0, 1, 2, 3, 4]: 
                print("Enter Valid mode number")
            else: 
                mode = choice 
                break
        except:
            print("Enter Valid mode number")

    while (True):
        winning_value = handle_input("Please enter the number of points required to win :")
        try:
            winning_value = int(winning_value)
            if (winning_value <= 0):
                print("The winning value should be positive!")
            elif (winning_value > 1000):
                print("The winning value should be less than 1000!")
            elif (winning_value % 50 != 0):
                print("The winning value should be divisible by 50!")
            else:
                break
        except:
            winning_value = 1
            print("The winning value must be a number!")

    spades = Game(winning_value, mode)

    begin_msg = handle_input("The game will now start! Press any key to begin...")
    spades.run()

# Master method of script
def main():
    welcome()
    run_game()
    quit()

main()
#Source and adapted from https://github.com/ReillyBova/spades/blob/master/card.py
