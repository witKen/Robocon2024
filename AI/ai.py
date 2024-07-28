# Simple rule base AI for robocon 2024 inspired by connect 4 game.
# Link : https://www.youtube.com/watch?v=UYgyRArKDEs&list=PLFCB5Dp81iNV_inzM-R9AKkZZlePCZdtV

import numpy as np
import pygame
import sys
import time
import random
import math

class AI:

    def __init__(self):
        self.BLUE = (0,0,255)
        self.BLACK = (0,0,0)
        self.RED = (255,0,0)
        self.WHITE = (255,255,255)

        self.ROW_COUNT = 3
        self.COLUMN_COUNT = 5

        self.playerOneLastMoveTime = 0
        self.playerTwoLastMoveTime = 0


        self.playerOneLastBallObtainTime = 0
        self.playerTwoLastBallObtainTime = 0

        self.playerOneBallObtainTime = 13
        self.playerTwoBallObtainTime = 13

        self.playerOneMoveTime = 1
        self.playerTwoMoveTime = 1

        self.playerOneCurrentBall = 5
        self.playerTwoCurrentBall = 5

        self.playerOneReserveBall = 7
        self.playerTwoReserveBall = 7

        self.playerOneInDanger = False
        self.playerTwoInDanger = False

        self.dangerPosition = 0

        print("Please Select Your Team")
        print("1. Team Red")
        print("2. Team Blue")

        self.selectedTeam = int(input("Select Team: "))
        self.playerOne = self.RED
        self.playerTwo = self.BLUE

        self.playerOneBall = 0
        self.playerTwoBall = 0

        if self.selectedTeam == 1:
            self.playerOne = self.RED
            self.playerTwo = self.BLUE
            self.playerOneBall = 1
            self.playerTwoBall = 2
        else :
            self.playerOne = self.BLUE
            self.playerTwo = self.RED
            self.playerOneBall = 2
            self.playerTwoBall = 1

        self.silo = self.create_silo()
        self.print_silo(self.silo)
        self.game_over = False
        
        pygame.init()

        self.SQUARESIZE = 100

        self.width = self.COLUMN_COUNT * self.SQUARESIZE
        self.height = (self.ROW_COUNT + 1) * self.SQUARESIZE

        self.size = (self.width, self.height)

        self.RADIUS = int(self.SQUARESIZE/2 - 5)

        self.screen = pygame.display.set_mode(self.size)
        self.draw_silo(self.silo)
        pygame.display.update()

        self.myfont = pygame.font.SysFont("monospace", 40)
        

    def create_silo(self):
        silo = np.zeros((self.ROW_COUNT, self.COLUMN_COUNT))
        return silo
    def drop_ball(self, silo, row, col, ball):
        silo[row][col] = ball

    def is_valid_location(self, silo, col):
        return silo[self.ROW_COUNT - 1][col] == 0

    def get_next_open_row(self, silo, col):
        for r in range(self.ROW_COUNT):
            if silo[r][col] == 0:
                return r
            
    def print_silo(self, silo):
        print(np.flip(silo, 0))

    #mua vang
    def winning_move(self, silo, ball):
        
        playerOneScore = 0
        playerTwoScore = 0

        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT-2):
                if silo[r][c] == ball and silo[r+2][c] == ball:
                    if ball == 1:
                        playerOneScore += 1
                    elif ball == 2:
                        playerTwoScore += 1
                elif silo[r+1][c] == ball and silo[r+2][c] == ball:
                    if ball == 1:
                        playerOneScore += 1
                    elif ball == 2:
                        playerTwoScore += 1

        if playerOneScore == 3 or playerTwoScore == 3:
            return True
        
    
    def draw_silo(self, silo):
        for c in range(self.COLUMN_COUNT):
            for r in range (self.ROW_COUNT):
                pygame.draw.rect(self.screen, self.WHITE, (c*self.SQUARESIZE, r*self.SQUARESIZE + self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
                pygame.draw.circle(self.screen, self.BLACK, (int(c*self.SQUARESIZE + self.SQUARESIZE/2), int(r*self.SQUARESIZE + self.SQUARESIZE + self.SQUARESIZE/2)), self.RADIUS)

        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                if silo[r][c] == 1:
                    pygame.draw.circle(self.screen, self.RED, (int(c*self.SQUARESIZE + self.SQUARESIZE/2), self.height - int(r*self.SQUARESIZE + self.SQUARESIZE/2)), self.RADIUS)
                elif silo[r][c] == 2:
                    pygame.draw.circle(self.screen, self.BLUE, (int(c*self.SQUARESIZE + self.SQUARESIZE/2), self.height - int(r*self.SQUARESIZE + self.SQUARESIZE/2)), self.RADIUS)
        pygame.display.update()

    def is_silo_full(self, silo):
        check = 0
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                if silo[r][c] == 1 or silo[r][c] == 2:
                    check += 1
        if check == 15:
            return True
    
    def get_valid_locations(self, silo):
        valid_locations = []
        for col in range(self.COLUMN_COUNT):
            if self.is_valid_location(silo, col):
                valid_locations.append(col)
        return valid_locations

    def evaluate(self, silo):
        playerOneScore = 0
        playerTwoScore = 0

        for i in range(1,3):
            for c in range(self.COLUMN_COUNT):
                for r in range(self.ROW_COUNT):
                    if silo[r][c] == i:
                        if i == 1:
                            playerOneScore += 60
                        elif i == 2:
                            playerTwoScore += 60

        if self.playerOneBall == 1:
            if playerOneScore == playerTwoScore:
                return 0
            elif playerOneScore > playerTwoScore:
                return 1
            elif playerOneScore < playerTwoScore:
                return 2
        elif self.playerOneBall == 2:
            if playerOneScore == playerTwoScore:
                return 0
            elif playerOneScore > playerTwoScore:
                return 2
            elif playerOneScore < playerTwoScore:
                return 1
    
    def pick_best_move(self, silo, ball):
        valid_locations = self.get_valid_locations(silo)

        if not valid_locations:
            return None
        
        best_score = -10000
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = self.get_next_open_row(silo, col)
            temp_silo = silo.copy()
            self.drop_ball(temp_silo, row, col, ball)
            score = self.score_position(silo, temp_silo, ball)
            if score > best_score:
                best_score = score
                best_col = col
        return best_col

    def checkInDanger(self, silo, ball):
        score = 0

        reserveBalls = self.playerTwoCurrentBall
        currentBalls = self.playerTwoCurrentBall

        opp_ball = self.playerOneBall
        opp_reserveBalls = self.playerOneReserveBall
        opp_currentBalls = self.playerOneReserveBall
        
        if ball == self.playerOneBall:
            opp_ball = self.playerTwoBall
            reserveBalls = self.playerOneReserveBall
            currentBalls = self.playerOneReserveBall

            opp_reserveBalls = self.playerTwoCurrentBall
            opp_currentBalls = self.playerTwoCurrentBall

        opp_balls_count = 0
        team_balls_count = 0

        opp_score_points = 0
        team_score_points = 0

        opp_balls_bottom = 0
        team_balls_bottom = 0

        balls = 0

        for c in range(self.COLUMN_COUNT):
            if (silo[0][c] == opp_ball and silo[1][c] == opp_ball and silo [2][c] == opp_ball) or (silo[0][c] == opp_ball and silo[1][c] == ball and silo [2][c] == opp_ball):
                opp_score_points += 1
            if (silo[0][c] == ball and silo[1][c] == ball and silo [2][c] == ball) or (silo[0][c] == ball and silo[1][c] == opp_ball and silo [2][c] == ball):
                team_score_points += 1

            if (opp_score_points == 2 and silo[0][c] == opp_ball and silo[1][c] == 0 and silo[2][c] == 0 and opp_reserveBalls <= 5):
                # if(ball == self.playerTwoBall):
                #     print("opp score: ",opp_score_points,", opp reserve: ", opp_reserveBalls)
                self.dangerPosition = c
                if ball == self.playerOneBall:
                    self.playerOneInDanger = True
                else:
                    # print("Player Two In Danger")
                    self.playerTwoInDanger = True
                break
            elif (opp_score_points == 2 and silo[0][self.dangerPosition] == opp_ball and silo[1][self.dangerPosition] == opp_ball and silo[2][self.dangerPosition] == 0):
                if ball == self.playerOneBall:
                    self.playerOneInDanger = False
                else:
                    self.playerTwoInDanger = False

    def printCondition(self, silo, ball):

        score = 0

        opp_ball = self.playerOneBall
        
        if ball == self.playerOneBall:
            opp_ball = self.playerTwoBall

        opp_balls_count = 0
        team_balls_count = 0

        opp_score_points = 0
        team_score_points = 0

        opp_balls_bottom = 0
        team_balls_bottom = 0

        balls = 0

        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                if silo[r][c] == opp_ball:
                    opp_balls_count += 1
                    balls += 1
                elif silo[r][c] == ball:
                    team_balls_count += 1
                    balls += 1

            if (silo[0][c] == opp_ball and silo[1][c] == opp_ball and silo [2][c] == opp_ball) or (silo[0][c] == opp_ball and silo[1][c] == ball and silo [2][c] == opp_ball):
                opp_score_points += 1
            if (silo[0][c] == ball and silo[1][c] == ball and silo [2][c] == ball) or (silo[0][c] == ball and silo[1][c] == opp_ball and silo [2][c] == ball):
                team_score_points += 1
                
            if silo[0][c] == opp_ball:
                opp_balls_bottom += 1
            if silo[0][c] == ball:
                team_balls_bottom += 1

        if team_balls_bottom < 3 and opp_balls_bottom < 3:
            # print("Player: ", ball, " Status: Initial, Current Balls: ", currentBalls, ", Reserve Balls: ", reserveBalls)
            print("Player: ", ball, ", Status: Initialize")
        elif (opp_balls_bottom < 3 and opp_score_points < 2) or (team_score_points > opp_score_points) or (team_score_points == 2):
            # print("Player: ", ball, " Status: Attack, Current Balls: ", currentBalls, ", Reserve Balls: ", reserveBalls)
            print("Player: ", ball, ", Status: Attack")
        else:
            # print("Player: ", ball, " No Condition, Current Balls: ", currentBalls, ", Reserve Balls: ", reserveBalls)
            print("Player: ", ball, " Status: Defend")


    def score_position(self, silo, tmp_silo, ball):
        score = 0

        opp_ball = self.playerOneBall
        
        if ball == self.playerOneBall:
            opp_ball = self.playerTwoBall

        opp_balls_count = 0
        team_balls_count = 0

        opp_score_points = 0
        team_score_points = 0

        opp_balls_bottom = 0
        team_balls_bottom = 0

        balls = 0

        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                if silo[r][c] == opp_ball:
                    opp_balls_count += 1
                    balls += 1
                elif silo[r][c] == ball:
                    team_balls_count += 1
                    balls += 1

            if (silo[0][c] == opp_ball and silo[1][c] == opp_ball and silo [2][c] == opp_ball) or (silo[0][c] == opp_ball and silo[1][c] == ball and silo [2][c] == opp_ball):
                opp_score_points += 1
            if (silo[0][c] == ball and silo[1][c] == ball and silo [2][c] == ball) or (silo[0][c] == ball and silo[1][c] == opp_ball and silo [2][c] == ball):
                team_score_points += 1
                
            if silo[0][c] == opp_ball:
                opp_balls_bottom += 1
            if silo[0][c] == ball:
                team_balls_bottom += 1

        #Get early good ball position
        if team_balls_bottom < 3 and opp_balls_bottom < 3:
            for c in range(self.COLUMN_COUNT):
                if tmp_silo[0][c] == ball and tmp_silo[1][c] == opp_ball and tmp_silo[2][c] == ball: #1 2 1
                    score += 300
                elif tmp_silo[0][c] == opp_ball and tmp_silo[1][c] == opp_ball and tmp_silo[2][c] == ball: #2 2 1
                    score += 100
                elif tmp_silo[0][c] == ball and tmp_silo[1][c] == 0 and tmp_silo[2][c] == 0: # 1 0 0
                    score += 175

                if tmp_silo[0][c] == opp_ball and tmp_silo[1][c] == 0 and tmp_silo[2][c] == 0: # 2 0 0
                    score -= 4
        
        #Attack Mode
        elif (opp_balls_bottom < 3 and opp_score_points < 2) or (team_score_points > opp_score_points) or (team_score_points == 2):
            for c in range(self.COLUMN_COUNT):
                if tmp_silo[0][c] == ball and tmp_silo[1][c] == opp_ball and tmp_silo[2][c] == ball: # 1 2 1
                    score += 200
                elif tmp_silo[0][c] == ball and tmp_silo[1][c] == ball and tmp_silo[2][c] == ball: # 1 1 1
                    score += 175
                elif tmp_silo[0][c] == opp_ball and tmp_silo[1][c] == ball and tmp_silo[2][c] == ball: # 2 1 1
                    score += 150
                elif tmp_silo[0][c] == opp_ball and tmp_silo[1][c] == opp_ball and tmp_silo[2][c] == ball: # 2 2 1
                    score += 100
                elif tmp_silo[0][c] == ball and tmp_silo[1][c] == ball: # 1 1 0
                    score += 50
                elif tmp_silo [0][c] == ball and tmp_silo[1][c] == 0 and tmp_silo[2][c] == 0: # 1 0 0
                    score += 10
                
                elif tmp_silo [0][c] == opp_ball and tmp_silo[1][c] == ball: # 2 1 0
                    score -= 50
                
                if tmp_silo[0][c] == opp_ball and tmp_silo[1][c] == 0 and tmp_silo[2][c] == 0:
                        score -= 4
         
        #Defend Mode
        else:
            for c in range(self.COLUMN_COUNT):
                if tmp_silo[0][c] == opp_ball and tmp_silo[1][c] == opp_ball and tmp_silo[2][c] == ball: # 2 2 1
                    score += 300
                elif tmp_silo[0][c] == ball and tmp_silo[1][c] == opp_ball and tmp_silo[2][c] == ball: # 1 2 1
                    score += 175
                elif tmp_silo[0][c] == ball and tmp_silo[1][c] == ball and tmp_silo[2][c] == ball: # 1 1 1
                    score += 150
                elif tmp_silo[0][c] == opp_ball and tmp_silo[1][c] == ball and tmp_silo[2][c] == ball: # 2 1 1
                    score += 100
                elif tmp_silo[0][c] == ball and tmp_silo[1][c] == ball: # 1 1 0
                    score += 50
                elif tmp_silo [0][c] == ball and tmp_silo[1][c] == 0 and tmp_silo[2][c] == 0: # 1 0 0
                    score += 10
                elif tmp_silo [0][c] == opp_ball and tmp_silo[1][c] == ball: # 2 1 0
                    score -= 50
                
                if tmp_silo[0][c] == opp_ball and tmp_silo[1][c] == 0 and tmp_silo[2][c] == 0: 
                    score -= 4

        return score
        

    def main(self):
        while not self.game_over:    
            
            self.checkInDanger(self.silo, self.playerOneBall)
            self.checkInDanger(self.silo, self.playerTwoBall)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            #     elif event.type == pygame.KEYDOWN:
            #         current_time = time.time()
            #         if event.key == pygame.K_1:
            #             col = 0
            #             if current_time - self.playerOneLastMoveTime >= self.playerOneMoveTime:
            #                 if self.is_valid_location(self.silo, col):
            #                     self.playerOneLastMoveTime = current_time
            #                     row = self.get_next_open_row(self.silo, col)
            #                     self.drop_ball(self.silo, row, col, self.playerOneBall)
            #         elif event.key == pygame.K_2:
            #             col = 1
            #             if current_time - self.playerOneLastMoveTime >= self.playerOneMoveTime:
            #                 if self.is_valid_location(self.silo, col):
            #                     self.playerOneLastMoveTime = current_time
            #                     row = self.get_next_open_row(self.silo, col)
            #                     self.drop_ball(self.silo, row, col, self.playerOneBall)
            #         elif event.key == pygame.K_3:
            #             col = 2
            #             if current_time - self.playerOneLastMoveTime >= self.playerOneMoveTime:
            #                 if self.is_valid_location(self.silo, col):
            #                     self.playerOneLastMoveTime = current_time
            #                     row = self.get_next_open_row(self.silo, col)
            #                     self.drop_ball(self.silo, row, col, self.playerOneBall)
            #         elif event.key == pygame.K_4:
            #             col = 3
            #             if current_time - self.playerOneLastMoveTime >= self.playerOneMoveTime:
            #                 if self.is_valid_location(self.silo, col):
            #                     self.playerOneLastMoveTime = current_time
            #                     row = self.get_next_open_row(self.silo, col)
            #                     self.drop_ball(self.silo, row, col, self.playerOneBall)
            #         elif event.key == pygame.K_5:
            #             col = 4
            #             if current_time - self.playerOneLastMoveTime >= self.playerOneMoveTime:
            #                 if self.is_valid_location(self.silo, col):
            #                     self.playerOneLastMoveTime = current_time
            #                     row = self.get_next_open_row(self.silo, col)
            #                     self.drop_ball(self.silo, row, col, self.playerOneBall)
                    
            #         if self.winning_move(self.silo, self.playerOneBall):
            #             print("Player One Win")
            #             label = self.myfont.render("Player One Win", 1, self.playerOne)
            #             self.screen.blit(label, (40, 10))
            #             self.game_over = True
                        
            #         self.print_silo(self.silo)
            #         self.draw_silo(self.silo)

            if not self.game_over and self.playerOneInDanger == False:
                current_time = time.time()
                # col = random.randint(0, self.COLUMN_COUNT-1)
                col = self.pick_best_move(self.silo, self.playerOneBall)
                
                if current_time - self.playerOneLastMoveTime >= self.playerOneMoveTime and self.playerOneCurrentBall > 0:
                    if self.is_valid_location(self.silo, col):
                        self.playerOneLastMoveTime = current_time
                        row = self.get_next_open_row(self.silo, col)
                        
                        self.printCondition(self.silo, self.playerOneBall)

                        self.drop_ball(self.silo, row, col, self.playerOneBall)

                        self.playerOneCurrentBall -= 1
                        
                        self.print_silo(self.silo)
                        # print("Player One Current Ball: ", self.playerOneCurrentBall)
                        if self.winning_move(self.silo, self.playerOneBall):
                            print("Player One Win")
                            label = self.myfont.render("Player One Win", 1, self.playerOne)
                            self.screen.blit(label, (40, 10))
                            self.game_over = True
                        self.draw_silo(self.silo)    

                if current_time - self.playerOneLastBallObtainTime >= self.playerOneBallObtainTime and self.playerOneReserveBall > 0:
                    self.playerOneLastBallObtainTime = current_time
                    self.playerOneReserveBall -= 1
                    self.playerOneCurrentBall += 1
                    print("Player One Reserve Ball: ", self.playerOneReserveBall)
                
                if self.is_silo_full(self.silo) and not self.winning_move(self.silo, self.playerOneBall) and not self.winning_move(self.silo, self.playerTwoBall):
                    result = self.evaluate(self.silo)
                    if result == 0:
                        print("Draw")
                        label = self.myfont.render("Draw", 1, self.WHITE)
                        self.screen.blit(label, (40, 10))
                    elif result == 1:
                        print("Player One Win")
                        label = self.myfont.render("Player One Win", 1, self.playerOne)
                        self.screen.blit(label, (40, 10))
                    elif result == 2:
                        print("Player Two Win")
                        label = self.myfont.render("Player Two Win", 1, self.playerTwo)
                        self.screen.blit(label, (40, 10))
                    self.game_over = True
                

            if not self.game_over and self.playerTwoInDanger == False:
                current_time = time.time()

                # col = random.randint(0, self.COLUMN_COUNT-1)
                col = self.pick_best_move(self.silo, self.playerTwoBall)
                
                if current_time - self.playerTwoLastMoveTime >= self.playerTwoMoveTime and self.playerTwoCurrentBall > 0:
                    if self.is_valid_location(self.silo, col):
                        self.playerTwoLastMoveTime = current_time
                        row = self.get_next_open_row(self.silo, col)
                        
                        self.printCondition(self.silo, self.playerTwoBall)

                        self.drop_ball(self.silo, row, col, self.playerTwoBall)
                        
                        self.playerTwoCurrentBall-=1
                        
                        self.print_silo(self.silo)
                        # print("Player Two Current Ball: ", self.playerTwoCurrentBall)
                        if self.winning_move(self.silo, self.playerTwoBall):
                            print("Player Two Win")
                            label = self.myfont.render("Player Two Win", 1, self.playerTwo)
                            self.screen.blit(label, (40, 10))
                            self.game_over = True
                        self.draw_silo(self.silo)    
                        
                if current_time - self.playerTwoLastBallObtainTime >= self.playerTwoBallObtainTime and self.playerTwoReserveBall > 0:
                    self.playerTwoLastBallObtainTime = current_time
                    self.playerTwoReserveBall -= 1
                    self.playerTwoCurrentBall += 1
                    # print("Player Two Reserve Ball: ", self.playerTwoReserveBall)
                    

                if self.is_silo_full(self.silo) and not self.winning_move(self.silo, self.playerOneBall) and not self.winning_move(self.silo, self.playerTwoBall):
                    result = self.evaluate(self.silo)
                    if result == 0:
                        print("Draw")
                        label = self.myfont.render("Draw", 1, self.WHITE)
                        self.screen.blit(label, (40, 10))
                    elif result == 1:
                        print("Player One Win")
                        label = self.myfont.render("Player One Win", 1, self.playerOne)
                        self.screen.blit(label, (40, 10))
                    elif result == 2:
                        print("Player Two Win")
                        label = self.myfont.render("Player Two Win", 1, self.playerTwo)
                        self.screen.blit(label, (40, 10))
                    self.game_over = True

            if self.game_over:
                while(1):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                self.print_silo(self.silo)
                print("Game Over")

if __name__ == "__main__":
    ai = AI()
    ai.main()



        
