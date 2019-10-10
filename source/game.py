from source.map import *
from source.graphics import *
from algorithms.BFS import *
from algorithms.Astar import *


class Game(Thread):
    def __init__(self, _screen):
        super().__init__()
        self.map = Map("testcases/test2")
        self.screen = _screen
        self.startPoint = self.map.getCell(4, 3)
        print(self.startPoint)
        self.graphics = Graphics(_screen, {'col': 6, 'row': 10})
        self.__stopped = False
        self.started_algorithm = False



    def run(self):
        while not self.__stopped:
            self.loop()
            self.draw()
            pg.display.update()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__stopped = True
                    break

    def loop(self):
        if not self.started_algorithm:
            self.started_algorithm = True
            Astar(self.map, self.startPoint, self.map.getCell(1, 8)).start()

    def draw(self):
        self.graphics.drawBoard()
        self.graphics.drawLines()
        self.graphics.drawCells(self.map)

