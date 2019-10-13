from source.game import *
import sys

sys.setrecursionlimit(50000)

ui = True

if ui:
    size = [300, 500]
    FULL_SCREEN = pg.DOUBLEBUF | pg.FULLSCREEN
    NORMAL = pg.DOUBLEBUF | pg.RESIZABLE
    pg.init()

    screen = pg.display.set_mode(size, NORMAL)

    game = Game(screen, ui)
    game.start()

else:
    game = Game(None, ui)
    game.start()
