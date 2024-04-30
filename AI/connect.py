# import numpy as np
# import pygame
# import sys
# import math

# BLUE = (0,0,255)
# BLACK = (0,0,0)
# RED = (255,0,0)
# WHITE = (255,255,255)

# ROW_COUNT = 3
# COLUMN_COUNT = 5

# def create_board():
#     board = np.zeros((ROW_COUNT,COLUMN_COUNT))
#     return board

# def drop_piece(board, row, col, piece):
#     board[row][col] = piece

# def is_valid_location(board, col):
#     return board[ROW_COUNT - 1][col] == 0

# def get_next_open_row(board, col):
#     for r in range(ROW_COUNT):
#         if board[r][col] == 0:
#             return r
        
# def print_board(board):
#     print(np.flip(board, 0))

# def winning_move(board, piece):
    
#     playerOneScore = 0
#     playerTwoScore = 0
#     for c in range(COLUMN_COUNT):
#         for r in range(ROW_COUNT-2):
#             if board[r][c] == piece and board[r+2][c] == piece:
#                 if piece == 1:
#                     playerOneScore += 1
#                 elif piece == 2:
#                     playerTwoScore += 1
#             elif board [r+1][c] == piece and board[r+2][c] == piece:
#                 if piece == 1:
#                     playerOneScore += 1
#                 elif piece == 2:
#                     playerTwoScore += 1
    
#     if playerOneScore == 3 or playerTwoScore == 3:
#         return True

# def draw_board(board):
#     for c in range (COLUMN_COUNT):
#         for r in range (ROW_COUNT):
#             pygame.draw.rect(screen, WHITE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
#             pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)

#     for c in range(COLUMN_COUNT):
#         for r in range (ROW_COUNT):
#             if board[r][c] == 1:
#                 pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
#             elif board[r][c] == 2:
#                 pygame.draw.circle(screen, BLUE, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)

#     pygame.display.update()


# board = create_board()
# print_board(board)
# game_over = False
# turn = 0

# pygame.init()

# SQUARESIZE = 100

# width = COLUMN_COUNT * SQUARESIZE
# height = (ROW_COUNT+1) * SQUARESIZE

# size = (width, height)

# RADIUS = int(SQUARESIZE/2 - 5)

# screen = pygame.display.set_mode(size)
# draw_board(board)
# pygame.display.update()

# myfont = pygame.font.SysFont("monospace", 40)

# while not game_over:

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()

#         if event.type == pygame.MOUSEMOTION:
#             pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
#             posx = event.pos[0]
#             if turn == 0:
#                 pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
#             elif turn == 1:
#                 pygame.draw.circle(screen, BLUE, (posx, int(SQUARESIZE/2)), RADIUS)
#         pygame.display.update()

#         if event.type == pygame.MOUSEBUTTONDOWN:
#             pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
#             if turn == 0:
#                 posx = event.pos[0]
#                 col = int(math.floor(posx/SQUARESIZE))

#                 if is_valid_location(board, col):
#                     row = get_next_open_row(board, col)
#                     drop_piece(board, row, col, 1)

#                     if winning_move(board, 1):
#                         label = myfont.render("Player 1 Win",1 , RED)
#                         screen.blit(label, (40, 10))
#                         game_over = True
            
#             else: 
#                 posx = event.pos[0]
#                 col = int(math.floor(posx/SQUARESIZE))

#                 if is_valid_location(board, col):
#                     row = get_next_open_row(board, col)
#                     drop_piece(board, row, col, 2)
            
#                 if winning_move(board, 2):
#                         label = myfont.render("Player 2 Win",1 , BLUE)
#                         screen.blit(label, (40, 10))
#                         game_over = True

#             draw_board(board)
#             turn += 1
#             turn = turn % 2

#             if game_over:
#                 pygame.time.wait(3000)

import numpy as np
import pygame
import sys
import time

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
WHITE = (255,255,255)

ROW_COUNT = 3
COLUMN_COUNT = 5

playerOneLastMoveTime = 0
playerTwoLastMoveTime = 0

playerOneMoveTime = 4
playerTwoMoveTime = 2

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
                        drop_piece(board, row, col, 1)
                        if winning_move(board, 1):
                            label = myfont.render("Player 1 Win",1 , RED)
                            screen.blit(label, (40, 10))
                            game_over = True
            elif event.key == pygame.K_2:
                col = 1
                if is_valid_location(board, col):
                    if current_time - playerOneLastMoveTime >= playerOneMoveTime:
                        playerOneLastMoveTime = current_time
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)
                        if winning_move(board, 1):
                            label = myfont.render("Player 1 Win",1 , RED)
                            screen.blit(label, (40, 10))
                            game_over = True
            elif event.key == pygame.K_3:
                col = 2
                if is_valid_location(board, col):
                    if current_time - playerOneLastMoveTime >= playerOneMoveTime:
                        playerOneLastMoveTime = current_time
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)
                        if winning_move(board, 1):
                            label = myfont.render("Player 1 Win",1 , RED)
                            screen.blit(label, (40, 10))
                            game_over = True
            elif event.key == pygame.K_4:
                col = 3
                if is_valid_location(board, col):
                    if current_time - playerOneLastMoveTime >= playerOneMoveTime:
                        playerOneLastMoveTime = current_time
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)
                        if winning_move(board, 1):
                            label = myfont.render("Player 1 Win",1 , RED)
                            screen.blit(label, (40, 10))
                            game_over = True
            elif event.key == pygame.K_5:
                col = 4
                if is_valid_location(board, col):
                    if current_time - playerOneLastMoveTime >= playerOneMoveTime:
                        playerOneLastMoveTime = current_time
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)
                        if winning_move(board, 1):
                            label = myfont.render("Player 1 Win",1 , RED)
                            screen.blit(label, (40, 10))
                            game_over = True

            if event.key == pygame.K_q:
                col = 0
                if is_valid_location(board, col):
                    if current_time - playerTwoLastMoveTime >= playerTwoMoveTime:
                        playerTwoLastMoveTime = current_time
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)
                        if winning_move(board, 2):
                            label = myfont.render("Player 2 Win",1 , BLUE)
                            screen.blit(label, (40, 10))
                            game_over = True
            elif event.key == pygame.K_w:
                col = 1
                if is_valid_location(board, col):
                    if current_time - playerTwoLastMoveTime >= playerTwoMoveTime:
                        playerTwoLastMoveTime = current_time
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)
                        if winning_move(board, 2):
                            label = myfont.render("Player 2 Win",1 , BLUE)
                            screen.blit(label, (40, 10))
                            game_over = True
            elif event.key == pygame.K_e:
                col = 2
                if is_valid_location(board, col):
                    if current_time - playerTwoLastMoveTime >= playerTwoMoveTime:
                        playerTwoLastMoveTime = current_time
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)
                        if winning_move(board, 2):
                            label = myfont.render("Player 2 Win",1 , BLUE)
                            screen.blit(label, (40, 10))
                            game_over = True
            elif event.key == pygame.K_r:
                col = 3
                if is_valid_location(board, col):
                    if current_time - playerTwoLastMoveTime >= playerTwoMoveTime:
                        playerTwoLastMoveTime = current_time
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)
                        if winning_move(board, 2):
                            label = myfont.render("Player 2 Win",1 , BLUE)
                            screen.blit(label, (40, 10))
                            game_over = True
            elif event.key == pygame.K_t:
                col = 4
                if is_valid_location(board, col):
                    if current_time - playerTwoLastMoveTime >= playerTwoMoveTime:
                        playerTwoLastMoveTime = current_time
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)
                        if winning_move(board, 2):
                            label = myfont.render("Player 2 Win",1 , BLUE)
                            screen.blit(label, (40, 10))
                            game_over = True
        

        draw_board(board)

        if is_board_full(board) and not winning_move(board,1) and not winning_move(board, 2):
            label = myfont.render("Draw",1 , WHITE)
            print("Draw")
            screen.blit(label, (40, 10))
            game_over = True

    if game_over:
        pygame.time.wait(3000)