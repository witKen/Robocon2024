import numpy as np

ROW_COUNT = 3
COLUMN_COUNT = 5

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
        
def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    
    playerOneScore = 0
    playerTwoScore = 0
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-2):
            if board[r][c] == piece and board[r+2][c] == piece:
                if piece == 1:
                    playerOneScore += 1
                elif piece == 2:
                    playerTwoScore += 1
            elif board [r+1][c] == piece and board[r+2][c] == piece:
                if piece == 1:
                    playerOneScore += 1
                elif piece == 2:
                    playerTwoScore += 1
    
    if playerOneScore == 3 or playerTwoScore == 3:
        return True


board = create_board()
print_board(board)
game_over = False
turn = 0

while not game_over:

    if turn == 0:
        col = int(input("Player 1 Make your Selection (0-2):"))

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)

            if winning_move(board, 1):
                print("Player 1 Win")
                game_over = True
    
    else: 
        col = int(input("Player 2 Make your Selection (0-2):"))

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)
    
        if winning_move(board, 2):
                print("Player 2 Win")
                game_over = True
    print_board(board)

    turn += 1
    turn = turn % 2
print(board)