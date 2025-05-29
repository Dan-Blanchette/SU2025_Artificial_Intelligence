ROWS = 6
COLUMNS = 7
EMPTY = '0' 


def create_board():
    return [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    for row in board:
        print(' '.join(row))
    print(' '.join([str(i) for i in range(COLUMNS)]))