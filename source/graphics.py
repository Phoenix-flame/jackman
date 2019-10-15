import pygame as pg


COLOR_WHITE = 255, 255, 255
COLOR_WALL = 72, 72, 72
COLOR_START = 236, 43, 24
COLOR_GOAL = 44, 234, 77
COLOR_VISITED = 200, 200, 200
COLOR_FOOD1 = 240, 234, 54
COLOR_FOOD2 = 241, 90, 207
COLOR_FOOD3 = 37, 138, 213

map_state = {'%': COLOR_WALL,
             '*': COLOR_FOOD3,
             'P': COLOR_START,
             'Q': COLOR_GOAL,
             ' ': COLOR_WHITE,
             '1': COLOR_FOOD1,
             '2':COLOR_FOOD2,
             '3':COLOR_FOOD3}


class Graphics:
    def __init__(self, screen, size):

        self.screen = screen
        self.cols = size['col']
        self.rows = size['row']
        self.size = 30
        self.screen = pg.display.set_mode([self.cols*self.size + 5, self.rows*self.size + 5], pg.RESIZABLE)

    def drawCells(self, _map):
        pg.font.init()
        _cell_offset = 5
        myfont = pg.font.SysFont('FreeSans', 10)
        for cell in _map.map.values():
            _x1 = (self.size - 0) * cell.x
            _y1 = (self.size - 0) * cell.y

            _text_offset_x = 20
            _text_offset_y = 13

            pg.draw.rect(self.screen, map_state[cell.getType()], (_x1 + _cell_offset, _y1 + _cell_offset,
                                                                  self.size - _cell_offset, self.size - _cell_offset))
            # textsurface = myfont.render(str(cell.x) + " " + str(cell.y), False, (0, 0, 0))
            # self.screen.blit(textsurface, (_x1 + _text_offset_x, _y1 + _text_offset_y))
            if cell.getType() == '1':
                textsurface = myfont.render('1', False, (0, 0, 0))
                self.screen.blit(textsurface,(_x1 + _text_offset_x, _y1 + _text_offset_y))
            elif cell.getType() == '2':
                textsurface = myfont.render('2', False, (0, 0, 0))
                self.screen.blit(textsurface,(_x1 + _text_offset_x, _y1 + _text_offset_y))
            elif cell.getType() == '3':
                textsurface = myfont.render('3', False, (0, 0, 0))
                self.screen.blit(textsurface, (_x1 + _text_offset_x, _y1 + _text_offset_y))

    def drawBoard(self):
        self.screen.fill(COLOR_WALL)

    def drawLines(self):
        for i in range(self.cols):
            pg.draw.line(self.screen, COLOR_WALL, (self.size*i, 0), (self.size*i, 500))
        for j in range(self.rows):
            pg.draw.line(self.screen, COLOR_WALL, (0, self.size*j), (300, self.size*j))

