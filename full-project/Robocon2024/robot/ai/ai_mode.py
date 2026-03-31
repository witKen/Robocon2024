import numpy as np
import pygame
import sys
from file_handling.file_handling import TeamSelectionHandler as tsh

class AI:

    def __init__(self, silo):

        self.ROW_COUNT = 3
        self.COLUMN_COUNT = 5

        self.selectedTeam = tsh.readTeamFile(self)

        self.playerOneBall = 0
        self.playerTwoBall = 0

        if self.selectedTeam == 1:
            self.playerOneBall = 1
            self.playerTwoBall = 2
        else :
            self.playerOneBall = 2
            self.playerTwoBall = 1

        self.silo = silo
        self.print_silo(self.silo)
        self.game_over = False
        
        pygame.init()

        self.SQUARESIZE = 100

        self.width = self.COLUMN_COUNT * self.SQUARESIZE
        self.height = (self.ROW_COUNT + 1) * self.SQUARESIZE

        self.size = (self.width, self.height)

        self.RADIUS = int(self.SQUARESIZE/2 - 5)
        
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

    def run_ai(self):
        self.print_silo(self.silo)  
            


        