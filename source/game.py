from source.map import *
from source.graphics import *

from algorithms.AStar import *
from algorithms.BFS import *
from algorithms.IDS import *

class Game(Thread):
    def __init__(self, _screen, ui=False):
        super().__init__()
        self.map = Map("testcases/test1")
        self.ui = ui
        self.graphics = None
        if ui:
            self.graphics = Graphics(_screen, {'col': self.map.cols, 'row': self.map.rows})
        self.__stopped = False
        self.started_algorithm = False

    def run(self):
        while not self.__stopped:
            self.loop()
            if self.ui:
                self.draw()
                pg.display.update()
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.__stopped = True
                        break

    def loop(self):
        if not self.started_algorithm:
            time = 0
            self.started_algorithm = True
            for i in range(3):
                tmp = BFS(self.map)
                tmp.start()
                tmp.join()
                time += tmp.time
            print(time/3.0)

    def draw(self):
        self.graphics.drawBoard()
        self.graphics.drawCells(self.map)

