# Author: Dan Blanchette
# Class: AI - Dr.Soule CS 570
# Date: 6-19-25
# Credits/Sources:
# https://www.geeksforgeeks.org/dsa/finding-optimal-move-in-tic-tac-toe-using-minimax-algorithm-in-game-theory/ 
# https://www.geeksforgeeks.org/dsa/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
# ChatGPT for debugging and explainations


ROWS = 6
COLUMNS = 7
EMPTY = '0' 


def create_board():
    return [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    for row in board:
        print(' '.join(row))
    print(' '.join([str(i) for i in range(COLUMNS)]))