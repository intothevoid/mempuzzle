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
    revealed_boxes = generate_revealed_boxes_data(False)

    first_selection = None  # store the (x,y) of the first box clicked

    DISPLAYSURF.fill(BGCOLOUR)
    start_game_animation(main_board)

    while True:
        DISPLAYSURF.fill(BGCOLOUR)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generate_revealed_boxes_data(val):
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


def split_into_groups_of(group_size, the_list):
    result = []
    for i in range(0, len(the_list), group_size):
        result.append(the_list[i:i + group_size])
    return result


def reveal_boxes_animation(board, boxes_to_reveal):
    # do the box reveal animation
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        draw_box_covers(board, boxes_to_reveal, coverage)


def cover_boxes_animation(board, boxes_to_cover):
    # do the cover animation
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        draw_box_covers(board, boxes_to_cover, coverage)


def draw_board(board, revealed):
    # draw boxes in covered or revealed state
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = left_top_coords_of_box(boxx, boxy)
            if not revealed[boxx][boxy]:
                # draw a covered box
                pygame.draw.rect(DISPLAYSURF, BOXCOLOUR,
                                 (left, top, BOXSIZE, BOXSIZE))
            else:
                # draw an icon
                shape, colour = get_shape_and_colour(boxx, boxy)
                draw_icon(shape, colour, boxx, boxy)


def draw_highlight_box(boxx, boxy):
    left, top = left_top_coords_of_box(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOUR, (left - 5,
                                                    top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def start_game_animation(board):
    # randomly reveal boxes, 8 at a time
    covered_boxes = generate_revealed_boxes_data(False)
    boxes = []

    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append((x, y))

    random.shuffle(boxes)

    box_groups = split_into_groups_of(8, boxes)

    draw_board(board, covered_boxes)
    for box_group in box_groups:
        reveal_boxes_animation(board, box_group)
        cover_boxes_animation(board, box_group)


if __name__ == "__main__":
    main()
