import enum

class CellType(enum.Enum):
    WALL = 1
    PLAYER1 = 2
    PLAYER2 = 3
    FOOD1 = 4
    FOOD2 = 5
    FOOD3 = 6
    EMPTY = -1


class Cell:
    def __init__(self, x, y, cellType=CellType.EMPTY):
        self.x = x
        self.y = y
        self.cellType = cellType

    def generateNeighbors(self):
        pass

    def getNeighbors(self):
        pass

    def changeType(self, newType):
        if self.cellType == CellType.WALL or self.cellType == CellType.PLAYER1 or self.cellType == CellType.PLAYER2:
            return
        self.cellType = newType


