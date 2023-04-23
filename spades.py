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


def show_rules(msg, type):

    rules = ("Spades is a fun & competitive card game for four (4) players split into two (2) teams. \n\n"
             "You can find the rules here : https://en.wikipedia.org/wiki/Spades_(card_game)#Rules \n"
             "Press any key to return to the game...\n"
             ">>>"
             )
    input(rules)
  
    return handle_input(msg, type)

def handle_input(msg, type=(CONTINUE)):
    response = input(msg + "\n>>>")
    if (response == QUIT):
        return kill_game(msg, type)
    elif (response == RULES):
        return show_rules(msg, type)
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

# Welcome message for the user
def welcome():
    os.system("clear")
    print(HEADER)
    hello_msg = ("Welcome to Spades Game! 1 Human Player and 3 AI Agent will be playing here! \nTo Quit: you may enter 'q' to quit and To read rules: 'r' to read the rules.\n\n"
                 "Note: Press 'Enter' key after typing your inputs in order to submit it to the game ")
    handle_input(hello_msg)

# Handles game setup and invokes play
def run_game():
    # Select the winning value
    winning_value = 1
    while (True):
        winning_value = handle_input("Please enter the number of points required to win (traditionally 500):")
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

    spades = Game(winning_value)

    begin_msg = handle_input("The game will now start! Press any key to begin...")
    spades.run()

# Master method of script
def main():
    welcome()
    run_game()
    quit()

main()
