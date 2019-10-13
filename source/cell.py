from enum import Enum


class Player(Enum):
    P = 1
    Q = 2


class Cell:
    def __init__(self, x, y, cellType='%', free=True):
        self.x = x
        self.y = y
        self.cellType = cellType
        self.free = free

        self.f = 0
        self.g = 0
        self.h = 0

    def changeType(self, newType):
        self.cellType = newType

    def getType(self):
        return self.cellType

    def getKey(self):
        return self.x, self.y

    def isFree(self, player=None):
        if player is None:
            return self.free
        if player == Player.P:
            if self.cellType == 'Q':
                return False
            return True
        if player == Player.Q:
            if self.cellType == 'P':
                return False
            return True

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + ", " + self.cellType + "]"



