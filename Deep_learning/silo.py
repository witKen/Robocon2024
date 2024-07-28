import heapq
import numpy as np

class Silo:
    def __init__(self) -> None:
        self._silo = [[None] * 3 for _ in range(5)]
        print(self._silo)

    # Return from sensors data
    def updateBoard(self, values:list) -> None:
        if (len(values) != 5):
            raise ValueError('There should only be 5 columns')
        if (len(values[0]) != 5):
            raise ValueError('There should only be 3 rows')
        
        for i in range(5):
            for j in range(3):
                self._silo[i][j] = values[i][j]

if __name__ == "__main__":
    silo = Silo()