# Author: Dan Blanchette
# Class: AI - Dr.Soule CS 570
# Date: 6-19-25
# Credits/Sources:
# https://www.geeksforgeeks.org/dsa/finding-optimal-move-in-tic-tac-toe-using-minimax-algorithm-in-game-theory/ 
# https://www.geeksforgeeks.org/dsa/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
# ChatGPT for debugging and explainations

import connectFourBoard as cfb



def is_valid_move(board, column):
    return board[0][column] == cfb.EMPTY

def make_move(board, column, piece):
    for row in reversed(board):
        if row[column] == cfb.EMPTY:
            row[column] = piece
            return

def check_win_state(board, piece):
    # Horizontal
    for row in range(cfb.ROWS):
        for col in range(cfb.COLUMNS - 3):
            if all(board[row][col + i] == piece for i in range(4)):
                return True
    # Vertical
    for col in range(cfb.COLUMNS):
        for row in range(cfb.ROWS - 3):
            if all(board[row + i][col] == piece for i in range(4)):
                return True
    # Positive diagonal
    for row in range(cfb.ROWS - 3):
        for col in range(cfb.COLUMNS - 3):
            if all(board[row + i][col + i] == piece for i in range(4)):
                return True
    # Negative diagonal
    for row in range(3, cfb.ROWS):
        for col in range(cfb.COLUMNS - 3):
            if all(board[row - i][col + i] == piece for i in range(4)):
                return True
    return False

def is_full(board):
    return all(cell != cfb.EMPTY for cell in board[0])

def main():
    board = cfb.create_board()
    current_player = 'X'
    cfb.print_board(board)

    while True:
        try:
            column = int(input(f"Player {current_player}, choose a column (0-{cfb.COLUMNS-1}): "))
            if column < 0 or column >= cfb.COLUMNS or not is_valid_move(board, column):
                print("Invalid move. Try again.")
                continue
            make_move(board, column, current_player)
            cfb.print_board(board)

            if check_win_state(board, current_player):
                print(f"Player {current_player} wins!")
                break
            if is_full(board):
                print("It's a draw!")
                break

            current_player = 'O' if current_player == 'X' else 'X'
        except ValueError:
            print("Please enter a valid number.")

if __name__ == '__main__':
    main()
