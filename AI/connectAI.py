import numpy as np
import pygame
import sys
import time
import random
import math

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
playerTwoMoveTime = 4

WINDOW_LENGTH = 3
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

#mua vang
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

def evaluate_window(window, piece):
    score = 0
    opp_piece = playerTeamPiece
    if piece == playerTeamPiece:
        opp_piece = enemyTeamPiece
    if window.count(piece) == 3:
        score += 100
    elif window.count(piece) == 1 and window.count(opp_piece) == 1 and window.count(EMPTY) == 1:
        score += 100
    elif window.count(piece) == 2 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 1 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 2 and window.count(EMPTY) == 1:
        score -= 4

    return score

def evaluate(board):
    playerOneScore = 0
    playerTwoScore = 0
    
    for i in range(1,3):
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-2):
                if board[r][c] == i:
                    if i == 1:
                        playerOneScore += 60
                    elif i == 2:
                        playerTwoScore += 60
    
    if playerTeamPiece == 1:
        if playerOneScore == playerTwoScore:
            return 0
        elif playerOneScore > playerTwoScore:
            return 1
        elif playerOneScore < playerTwoScore:
            return 2
    elif playerTeamPiece == 2:
        if playerOneScore == playerTwoScore:
            return 0
        elif playerOneScore > playerTwoScore:
            return 2
        elif playerOneScore < playerTwoScore:
            return 1

def score_position(board,tmp_board, piece):
    score = 0

    center_array = [int(1) for i in list(board[: , COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 6

    pieces = 0

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1 or board[r][c] == 2:
                pieces += 1    

    if pieces <= 5:
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(tmp_board[r,:])]
            for c in range(COLUMN_COUNT-3):
                window = row_array[c:c+WINDOW_LENGTH]
                # if window.count(piece) == 2:
                #     score += 100
                # elif window.count(piece) == 1 and window.count(EMPTY) == 0:
                #     score += 10

                # opp_piece = playerTeamPiece
                # if piece == playerTeamPiece:
                #     opp_piece = enemyTeamPiece
                # if window.count(piece) == 3:
                #     score += 100
                # elif window.count(piece) == 1 and window.count(opp_piece) == 1 and window.count(EMPTY) == 1:
                #     score += 100
                # elif window.count(piece) == 2 and window.count(EMPTY) == 1:
                #     score += 5
                # elif window.count(piece) == 1 and window.count(EMPTY) == 2:
                #     score += 2

                # if window.count(opp_piece) == 2 and window.count(EMPTY) == 1:
                #     score -= 4

                # return score


                score += evaluate_window(window, piece)

    # # for c in range(COLUMN_COUNT):
    # #     col_array = [int(i) for i in list(board[:,c])]
    # #     print(c, ": ",col_array)
    # #     for r in range(ROW_COUNT):
    # #         window = col_array[r:r+WINDOW_LENGTH]
    # #         print(r, ": ", window)

    elif pieces > 5:
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(tmp_board[:,c])]
            for r in range(ROW_COUNT):
                window = col_array[r:r+WINDOW_LENGTH]
                # if window.count(piece) == 3:
                #     score += 100
                # elif window.count(piece) == 2 and window.count(EMPTY) == 1:
                #     score += 10
                score += evaluate_window(window, piece)
    return score

def is_terminal_node(board):
    return winning_move(board, playerTeamPiece) or winning_move(board, enemyTeamPiece) or len(get_valid_locations(board)) == 0

def minimax(board, depth,alpha,beta,maximizingPlayer):
    is_valid_location = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, enemyTeamPiece):
                return (None, 100000000000000)
            elif winning_move(board, playerTeamPiece):
                return (None, -100000000000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, board,enemyTeamPiece))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(is_valid_location)
        for col in is_valid_location:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, enemyTeamPiece)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:
        value = math.inf
        column = random.choice(is_valid_location)
        for col in is_valid_location:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, playerTeamPiece)
            new_score = minimax(b_copy, depth-1,alpha,beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

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

    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(board,temp_board, piece)
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
                if current_time - playerOneLastMoveTime >= playerOneMoveTime:
                    if is_valid_location(board, col):
                        playerOneLastMoveTime = current_time
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, playerTeamPiece)
            elif event.key == pygame.K_2:
                col = 1
                if current_time - playerOneLastMoveTime >= playerOneMoveTime:
                    if is_valid_location(board, col):
                        playerOneLastMoveTime = current_time
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, playerTeamPiece)
            elif event.key == pygame.K_3:
                col = 2
                if current_time - playerOneLastMoveTime >= playerOneMoveTime:
                    if is_valid_location(board, col):
                        playerOneLastMoveTime = current_time
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, playerTeamPiece)
            elif event.key == pygame.K_4:
                col = 3
                if current_time - playerOneLastMoveTime >= playerOneMoveTime:
                    if is_valid_location(board, col):
                        playerOneLastMoveTime = current_time
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, playerTeamPiece)
            elif event.key == pygame.K_5:
                col = 4
                if current_time - playerOneLastMoveTime >= playerOneMoveTime:
                    if is_valid_location(board, col):
                        playerOneLastMoveTime = current_time
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, playerTeamPiece)
            if winning_move(board, playerTeamPiece):
                print("Player Win")
                label = myfont.render("Player Win",1 , playerTeam)
                screen.blit(label, (40, 10))
                game_over = True
            draw_board(board)

    if not game_over:
        current_time = time.time()
        
        # col = random.randint(0, COLUMN_COUNT-1)
        # col = pick_best_move(board, enemyTeamPiece)
        col, minimax_score = minimax(board, 2, -math.inf, math.inf,True)

        if current_time - playerTwoLastMoveTime >= playerTwoMoveTime:
            if is_valid_location(board, col):
                playerTwoLastMoveTime = current_time
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, enemyTeamPiece)
                print(col)
                print_board(board)
                if winning_move(board, enemyTeamPiece):
                    print("AI Win")
                    label = myfont.render("AI Win",1 , enemyTeam)
                    screen.blit(label, (40, 10))
                    game_over = True
                draw_board(board)

        if is_board_full(board) and not winning_move(board,playerTeamPiece) and not winning_move(board, enemyTeamPiece):
            result = evaluate(board)
            if result == 0:
                print("Draw")
                label = myfont.render("Draw",1 , WHITE)
                screen.blit(label, (40, 10))
            elif result == 1:
                print("Player Win")
                label = myfont.render("Player Win",1 , playerTeam)
                screen.blit(label, (40, 10))
            elif result == 2:
                print("AI Win")
                label = myfont.render("AI Win",1 , enemyTeam)
                screen.blit(label, (40, 10))
            game_over = True

    if game_over:
        print_board(board)
        print("game over")