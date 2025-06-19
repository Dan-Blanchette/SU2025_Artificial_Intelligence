# Author: Dan Blanchette
# Class: AI - Dr.Soule CS 570
# Date: 6-19-25
# Credits/Sources:
# https://www.geeksforgeeks.org/dsa/finding-optimal-move-in-tic-tac-toe-using-minimax-algorithm-in-game-theory/ 
# https://www.geeksforgeeks.org/dsa/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
# ChatGPT for debugging and explainations

import random
import math


ROWS = 6
COLUMNS = 7
EMPTY = '.'
MAX_DEPTH = 4  # Depth for minimax
WIN_SCORE = 1000000

class ConnectFourGame:
    def __init__(self):
        # Initialize the game board as a 6x7 grid of empty cells
        self.board = [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]

    def print_board(self):
        # Print the game board to the console
        for row in self.board:
            print(' '.join(row))
        print(' '.join([str(i) for i in range(COLUMNS)]))

    def is_valid_move(self, column):
        # Return True if a move can be made in the specified column
        return self.board[0][column] == EMPTY

    def make_move(self, column, piece):
        # Drop a piece into the specified column at the lowest available row
        for row in reversed(self.board):
            if row[column] == EMPTY:
                row[column] = piece
                return
            
    # Used by the agent to determine the best path to the goal
    # by "undoing" a move if traversal scoring during the DFS is 
    # not on the optimal branch.
    def undo_move(self, column):
        # Remove the topmost piece from the specified column
        for row in self.board:
            if row[column] != EMPTY:
                row[column] = EMPTY
                return

    def check_winner(self, piece):
        # Check for 4-in-a-row horizontally, vertically, and diagonally
        # Row check
        for row in range(ROWS):
            for col in range(COLUMNS - 3):
                if all(self.board[row][col + i] == piece for i in range(4)):
                    return True
                
        # Horizontal check
        for col in range(COLUMNS):
            for row in range(ROWS - 3):
                if all(self.board[row + i][col] == piece for i in range(4)):
                    return True

        # Pos Diagonal Direction       
        for row in range(ROWS - 3):
            for col in range(COLUMNS - 3):
                if all(self.board[row + i][col + i] == piece for i in range(4)):
                    return True
        # Neg Diagonal Direction
        for row in range(3, ROWS):
            for col in range(COLUMNS - 3):
                if all(self.board[row - i][col + i] == piece for i in range(4)):
                    return True
        return False

    def is_full(self):
        # Check if the board is completely filled
        return all(cell != EMPTY for cell in self.board[0])

    def get_valid_moves(self):
        # Return a list of column indices where a move can be made
        return [col for col in range(COLUMNS) if self.is_valid_move(col)]

    def score_position(self, piece):
        # Heuristic: favor placing pieces in the center column
        score = 0
        center_col = [self.board[row][COLUMNS // 2] for row in range(ROWS)]
        score += center_col.count(piece) * 3
        return score

    def is_terminal_node(self):
        # Return True if the game has ended (win or draw)
        return self.check_winner('X') or self.check_winner('O') or self.is_full()

class Player:
    def __init__(self, piece):
        self.piece = piece

    def get_move(self, game):
        raise NotImplementedError

class HumanPlayer(Player):
    def get_move(self, game):
        # Prompt the human player for a valid column input
        while True:
            try:
                column = int(input(f"Your move (0-{COLUMNS-1}): "))
                if 0 <= column < COLUMNS and game.is_valid_move(column):
                    return column
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Please enter a valid number.")

class MinimaxComputerPlayer(Player):
    def get_move(self, game):
        # Use the minimax algorithm to choose the best move
        _, column = self.minimax(game, MAX_DEPTH, -math.inf, math.inf, True)
        print(f"Computer ({self.piece}) chooses column {column}")
        return column

    def minimax(self, game, depth, alpha, beta, maximizing):
        # Recursive minimax algorithm with alpha-beta pruning
        # Chooses the best score assuming both players play optimally
        opponent_piece = 'O' if self.piece == 'X' else 'X'

        # Base case: if at a terminal node or depth limit
        if depth == 0 or game.is_terminal_node():
            if game.check_winner(self.piece):
                return (WIN_SCORE - (MAX_DEPTH - depth) * 1000, None)  # Prefer quicker wins
            elif game.check_winner(opponent_piece):
                return (-WIN_SCORE + (MAX_DEPTH - depth) * 1000, None)  # Prefer delayed losses
            else:
                return (game.score_position(self.piece), None)

        valid_moves = game.get_valid_moves()
        best_col = random.choice(valid_moves)

        if maximizing:
            # Maximizing player's turn (AI)
            value = -math.inf
            for col in valid_moves:
                game.make_move(col, self.piece)
                score, _ = self.minimax(game, depth - 1, alpha, beta, False)
                game.undo_move(col)
                if score > value:
                    value = score
                    best_col = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value, best_col
        else:
            # Minimizing player's turn (opponent)
            value = math.inf
            for col in valid_moves:
                game.make_move(col, opponent_piece)
                score, _ = self.minimax(game, depth - 1, alpha, beta, True)
                game.undo_move(col)
                if score < value:
                    value = score
                    best_col = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value, best_col

def main():
    game = ConnectFourGame()

    print("Player vs Computer")
    first_choice = input("Do you want to go first? (y/n): ").strip().lower()
    while first_choice not in ['y', 'n']:
        first_choice = input("Invalid input. Enter 'y' or 'n': ").strip().lower()

    if first_choice == 'y':
        human_player = HumanPlayer('X')
        ai_player = MinimaxComputerPlayer('O')
        player1 = human_player
        player2 = ai_player
    else:
        ai_player = MinimaxComputerPlayer('X')
        human_player = HumanPlayer('O')
        player1 = ai_player
        player2 = human_player

    current_player = player1
    game.print_board()

    while True:
        column = current_player.get_move(game)
        game.make_move(column, current_player.piece)
        game.print_board()

        if game.check_winner(current_player.piece):
            if isinstance(current_player, MinimaxComputerPlayer):
                print("Computer wins!")
            else:
                print("You win!")
            break

        if game.is_full():
            print("It's a draw!")
            break

        current_player = player1 if current_player == player2 else player2

if __name__ == '__main__':
    main()
