from source.map import *
from source.graphics import *
from algorithms.BFS import *
from algorithms.Astar import *
from algorithms.IDS import *


class Game(Thread):
    def __init__(self, _screen):
        super().__init__()
        self.map = Map("testcases/test4")
        self.graphics = Graphics(_screen, {'col': self.map.cols, 'row': self.map.rows})
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
            BFS(self.map, self.map.getCell(self.map.p), self.map.getCell(self.map.food1[0])).start()

    def draw(self):
        self.graphics.drawBoard()
        # self.graphics.drawLines()
        self.graphics.drawCells(self.map)

