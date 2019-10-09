from source.cell import *


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Map:
    def __init__(self, _dir):
        self.map_dir = _dir
        self.map = {}
        self.createMap()

    def createMap(self):
        with open(self.map_dir) as map_file:
            lines = map_file.readlines()

        for i, line in enumerate(lines):
            line = line.strip()
            for j, cell in enumerate(line):
                self.map[(i, j)] = Cell(i, j, cell)



    def getCell(self, x, y):
        return self.map[(x, y)]

    def getNextCell(self, curCell, direction):
        _x = curCell.x
        _y = curCell.y
        if direction == Direction.UP:
            try:
                return self.map[(_x, _y - 1)]
            except KeyError:
                return None
        elif direction == Direction.DOWN:
            try:
                return self.map[(_x, _y + 1)]
            except KeyError:
                return None
        elif direction == Direction.RIGHT:
            try:
                return self.map[(_x + 1, _y)]
            except KeyError:
                return None
        elif direction == Direction.LEFT:
            try:
                return self.map[(_x - 1, _y)]
            except KeyError:
                return None

    def getAdjacents(self, curCell):
        result = []
        for d in Direction:
            nextCell = self.getNextCell(curCell, d)
            if nextCell is not None:
                result.append(nextCell)
        return result


