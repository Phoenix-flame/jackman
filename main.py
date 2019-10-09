from source.game import *
from source.graphics import *

size = [300, 500]
pg.init()
FULL_SCREEN = pg.DOUBLEBUF | pg.FULLSCREEN
NORMAL = pg.DOUBLEBUF

screen = pg.display.set_mode(size, NORMAL)

game = Game(screen)
game.start()
