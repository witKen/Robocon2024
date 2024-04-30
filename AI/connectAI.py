import numpy as np
import pygame
import sys
import time
import random

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
WHITE = (255,255,255)

ROW_COUNT = 3
COLUMN_COUNT = 5

PLAYER = 0
AI = 1

playerOneLastMoveTime = 0
playerTwoLastMoveTime = 0

playerOneMoveTime = 1
playerTwoMoveTime = 1

WINDOW_LENGTH = 2
EMPTY = 0

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

def draw_board(board):
    for c in range (COLUMN_COUNT):
        for r in range (ROW_COUNT):
            pygame.draw.rect(screen, WHITE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range (ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, BLUE, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)

    pygame.display.update()

def is_board_full(board):
    check = 0
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1 or board[r][c] == 2:
                check += 1
    if check == 15:
        return True
    
def score_position(board, piece):

    score = 0
    
    # for r in range(ROW_COUNT):
    #     row_array = [int(i) for i in list(board[r,:])]
    #     for c in range(COLUMN_COUNT-3):
    #         window = row_array[c:c+WINDOW_LENGTH]
            
    #         if window.count(piece) == 2:
    #             score += 100
    #         elif window.count(piece) == 1 and window.count(EMPTY) == 1:
    #             score += 10
    
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT):
            window = col_array[r:r+WINDOW_LENGTH]
            
            if window.count(piece) == 2:
                score += 100
            elif window.count(piece) == 1 and window.count(EMPTY) == 1:
                score += 10
    
    return score

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)

    if not valid_locations:
        return None

    best_score = 0
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col

print("Please Select Your Team")
print("1. Team Red")
print("2. Team Blue")

selectedTeam = int(input("Select Team: "))
playerTeam = RED
enemyTeam = BLUE

playerTeamPiece = 0
enemyTeamPiece = 0

if selectedTeam == 1:
    playerTeam = RED
    enemyTeam = BLUE
    playerTeamPiece = 1
    enemyTeamPiece = 2
else :
    playerTeam = BLUE
    enemyTeam = RED
    playerTeamPiece = 2
    enemyTeamPiece = 1

board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 40)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            current_time = time.time()
            if event.key == pygame.K_1:
                col = 0
                if is_valid_location(board, col):
                    if current_time - playerOneLastMoveTime >= playerOneMoveTime:
                        playerOneLastMoveTime = current_time
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, playerTeamPiece)
                        if winning_move(board, playerTeamPiece):
                            label = myfont.render("Red Team Win",1 , playerTeam)
                            screen.blit(label, (40, 10))
                            game_over = True
            elif event.key == pygame.K_2:
                col = 1
                if is_valid_location(board, col):
                    if current_time - playerOneLastMoveTime >= playerOneMoveTime:
                        playerOneLastMoveTime = current_time
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, playerTeamPiece)
                        if winning_move(board, playerTeamPiece):
                            label = myfont.render("Red Team Win",1 , playerTeam)
                            screen.blit(label, (40, 10))
                            game_over = True
            elif event.key == pygame.K_3:
                col = 2
                if is_valid_location(board, col):
                    if current_time - playerOneLastMoveTime >= playerOneMoveTime:
                        playerOneLastMoveTime = current_time
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, playerTeamPiece)
                        if winning_move(board, playerTeamPiece):
                            label = myfont.render("Red Team Win",1 , playerTeam)
                            screen.blit(label, (40, 10))
                            game_over = True
            elif event.key == pygame.K_4:
                col = 3
                if is_valid_location(board, col):
                    if current_time - playerOneLastMoveTime >= playerOneMoveTime:
                        playerOneLastMoveTime = current_time
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, playerTeamPiece)
                        if winning_move(board, playerTeamPiece):
                            label = myfont.render("Red Team Win",1 , playerTeam)
                            screen.blit(label, (40, 10))
                            game_over = True
            elif event.key == pygame.K_5:
                col = 4
                if is_valid_location(board, col):
                    if current_time - playerOneLastMoveTime >= playerOneMoveTime:
                        playerOneLastMoveTime = current_time
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, playerTeamPiece)
                        if winning_move(board, playerTeamPiece):
                            label = myfont.render("Player Win",1 , playerTeam)
                            screen.blit(label, (40, 10))
                            game_over = True
            draw_board(board)

    if not game_over:
        current_time = time.time()
        
        # col = random.randint(0, COLUMN_COUNT-1)
        col = pick_best_move(board, enemyTeamPiece)

        if is_valid_location(board, col):
            if current_time - playerTwoLastMoveTime >= playerTwoMoveTime:
                playerTwoLastMoveTime = current_time
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, enemyTeamPiece)
                if winning_move(board, enemyTeamPiece):
                    label = myfont.render("AI Win",1 , enemyTeam)
                    screen.blit(label, (40, 10))
                    game_over = True
                draw_board(board)

        if is_board_full(board) and not winning_move(board,playerTeamPiece) and not winning_move(board, enemyTeamPiece):
            label = myfont.render("Draw",1 , WHITE)
            screen.blit(label, (40, 10))
            game_over = True

    if game_over:
        pygame.time.wait(3000)