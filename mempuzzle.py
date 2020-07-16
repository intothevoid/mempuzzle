import sys
import random
import pygame
from pygame import *

# constants
FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
REVEALSPEED = 8
BOXSIZE = 40
GAPSIZE = 10
BOARDWIDTH = 10
BOARDHEIGHT = 7
assert(BOARDHEIGHT * BOARDWIDTH) % 2 == 0, "Board needs to have an even no. of boxes for pairs of matches."
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
XMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

# R    G    B
GRAY = (100, 100, 100)
NAVYBLUE = (60,  60, 100)
WHITE = (255, 255, 255)
RED = (255,   0,   0)
GREEN = (0, 255,   0)
BLUE = (0,   0, 255)
YELLOW = (255, 255,   0)
ORANGE = (255, 128,   0)
PURPLE = (255,   0, 255)
CYAN = (0, 255, 255)
BGCOLOUR = NAVYBLUE
LIGHTBGCOLOUR = GRAY
BOXCOLOUR = WHITE
HIGHLIGHTCOLOUR = BLUE

# shapes
DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLOURS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLOURS) * len(ALLSHAPES) * 2 >= BOARDHEIGHT * \
    BOARDWIDTH, "Board is too big for the number of shapes / colours"


def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Memory Puzzle")

    main_board = get_randomised_board()
    revealed_boxes = get_revealed_boxes_data(False)

    DISPLAYSURF.fill(BGCOLOUR)

    while True:
        DISPLAYSURF.fill(BGCOLOUR)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def get_revealed_boxes_data(val):
    revealed_boxes = []
    for i in range(BOARDWIDTH):
        revealed_boxes.append([val] * BOARDHEIGHT)
    return revealed_boxes


def get_randomised_board() -> list:
    icons = []
    for colour in ALLCOLOURS:
        for shape in ALLSHAPES:
            icons.append((colour, shape))

    random.shuffle(icons)  # randomise the order of the icons

    # no. of icons that fit on board
    num_icons_used = int(BOARDHEIGHT * BOARDWIDTH / 2)
    icons = icons[:num_icons_used] * 2  # make two of each
    random.shuffle(icons)

    # create the board data structure, with randomly placed icons
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons.pop())

        board.append(column)

    return board


if __name__ == "__main__":
    main()
