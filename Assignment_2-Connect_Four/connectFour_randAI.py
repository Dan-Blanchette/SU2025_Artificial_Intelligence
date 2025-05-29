import random

ROWS = 6
COLUMNS = 7
EMPTY = '.'

# The ConnectFourGame class encapsulates all game logic and board management
class ConnectFourGame:
    def __init__(self):
        # Initialize a 6x7 board filled with EMPTY symbols
        self.board = [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]

    def print_board(self):
        # Print the current state of the board
        for row in self.board:
            print(' '.join(row))
        print(' '.join([str(i) for i in range(COLUMNS)]))

    def is_valid_move(self, column):
        # Check if a move in the selected column is valid (i.e., not full)
        return self.board[0][column] == EMPTY

    def make_move(self, column, piece):
        # Drop the player's piece in the lowest available row in the given column
        for row in reversed(self.board):
            if row[column] == EMPTY:
                row[column] = piece
                return

    def check_winner(self, piece):
        # Check all directions for a winning condition: horizontal, vertical, and diagonals
        for row in range(ROWS):
            for col in range(COLUMNS - 3):
                if all(self.board[row][col + i] == piece for i in range(4)):
                    return True
        for col in range(COLUMNS):
            for row in range(ROWS - 3):
                if all(self.board[row + i][col] == piece for i in range(4)):
                    return True
        for row in range(ROWS - 3):
            for col in range(COLUMNS - 3):
                if all(self.board[row + i][col + i] == piece for i in range(4)):
                    return True
        for row in range(3, ROWS):
            for col in range(COLUMNS - 3):
                if all(self.board[row - i][col + i] == piece for i in range(4)):
                    return True
        return False

    def is_full(self):
        # Return True if the top row is full (i.e., board is full)
        return all(cell != EMPTY for cell in self.board[0])

    def get_valid_moves(self):
        # Return a list of columns where a move is possible
        return [col for col in range(COLUMNS) if self.is_valid_move(col)]

# Base Player class. All players have a piece (either 'X' or 'O')
class Player:
    def __init__(self, piece):
        self.piece = piece

    def get_move(self, game):
        # This method should be overridden by subclasses
        raise NotImplementedError

# HumanPlayer prompts the user to choose a column on their turn
class HumanPlayer(Player):
    def get_move(self, game):
        while True:
            try:
                column = int(input(f"Player {self.piece}, choose a column (0-{COLUMNS-1}): "))
                if 0 <= column < COLUMNS and game.is_valid_move(column):
                    return column
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Please enter a valid number.")

# ComputerPlayer randomly chooses a valid column to make a move
class ComputerPlayer(Player):
    def get_move(self, game):
        column = random.choice(game.get_valid_moves())
        print(f"Computer ({self.piece}) chooses column {column}")
        return column

# Main function to handle game setup and loop

def main():
    game = ConnectFourGame()

    print("Choose game mode:")
    print("1. Two Player")
    print("2. Player vs Computer")
    mode = input("Enter 1 or 2: ").strip()

    # Ask the human which piece they want to be
    player_piece = input("Choose your piece (X or O): ").strip().upper()
    while player_piece not in ['X', 'O']:
        player_piece = input("Invalid choice. Please choose 'X' or 'O': ").strip().upper()

    computer_piece = 'O' if player_piece == 'X' else 'X'

    # Create appropriate player objects based on game mode
    if mode == '1':
        player1 = HumanPlayer('X')
        player2 = HumanPlayer('O')
    else:
        if player_piece == 'X':
            player1 = HumanPlayer('X')
            player2 = ComputerPlayer('O')
        else:
            player1 = ComputerPlayer('X')
            player2 = HumanPlayer('O')

    current_player = player1
    game.print_board()

    # Main game loop
    while True:
        column = current_player.get_move(game)
        game.make_move(column, current_player.piece)
        game.print_board()

        if game.check_winner(current_player.piece):
            if isinstance(current_player, ComputerPlayer):
                print("Computer wins!")
            else:
                print(f"Player {current_player.piece} wins!")
            break

        if game.is_full():
            print("It's a draw!")
            break

        # Switch turns
        current_player = player1 if current_player == player2 else player2

if __name__ == '__main__':
    main()
