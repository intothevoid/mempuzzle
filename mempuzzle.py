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
assert (BOARDHEIGHT * BOARDWIDTH) % 2 == 0, "Board needs to have an even no. of boxes for pairs of matches."
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

# R    G    B
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
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
    """
    main entry point of game
    """
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0
    mousey = 0
    pygame.display.set_caption("Memory Puzzle")

    main_board = get_randomised_board()
    revealed_boxes = generate_revealed_boxes_data(False)

    first_selection = None  # store the (x,y) of the first box clicked

    DISPLAYSURF.fill(BGCOLOUR)
    start_game_animation(main_board)

    # main game loop
    while True:
        mouse_clicked = False

        DISPLAYSURF.fill(BGCOLOUR)
        draw_board(main_board, revealed_boxes)

        # event loop
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouse_clicked = True

        boxx, boxy = get_box_at_pixel(mousex, mousey)
        if boxx != None and boxy != None:
            # The mouse is currently over a box.
            if not revealed_boxes[boxx][boxy]:
                draw_highlight_box(boxx, boxy)
            if not revealed_boxes[boxx][boxy] and mouse_clicked:
                reveal_boxes_animation(main_board, [(boxx, boxy)])
                revealed_boxes[boxx][boxy] = True  # set the box as "revealed"
                if first_selection is None:  # the current box was the first box clicked
                    first_selection = (boxx, boxy)
                else:  # the current box was the second box clicked
                    # Check if there is a match between the two icons.
                    icon1shape, icon1color = get_shape_and_colour(main_board, first_selection[0], first_selection[1])
                    icon2shape, icon2color = get_shape_and_colour(main_board, boxx, boxy)

                    if icon1shape != icon2shape or icon1color != icon2color:
                        # Icons don't match. Re-cover up both selections.
                        pygame.time.wait(1000)  # 1000 milliseconds = 1 sec
                        cover_boxes_animation(main_board, [(first_selection[0], first_selection[1]), (boxx, boxy)])
                        revealed_boxes[first_selection[0]][first_selection[1]] = False
                        revealed_boxes[boxx][boxy] = False
                    elif has_won(revealed_boxes):  # check if all pairs found
                        game_won_animation(main_board)
                        pygame.time.wait(2000)

                        # Reset the board
                        main_board = get_randomised_board()
                        revealed_boxes = generate_revealed_boxes_data(False)

                        # Show the fully unrevealed board for a second.
                        draw_board(main_board, revealed_boxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        # Replay the start game animation.
                        start_game_animation(main_board)
                    first_selection = None  # reset first_selection variable

        # Redraw the screen and wait a tick
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generate_revealed_boxes_data(val):
    revealed_boxes = []
    for i in range(BOARDWIDTH):
        revealed_boxes.append([val] * BOARDHEIGHT)
    return revealed_boxes


def get_randomised_board():
    icons = []
    for colour in ALLCOLOURS:
        for shape in ALLSHAPES:
            icons.append((shape, colour))

    random.shuffle(icons)  # randomise the order of the icons

    # no. of icons that fit on board
    num_icons_used = int(BOARDHEIGHT * BOARDWIDTH / 2)
    icons = icons[:num_icons_used] * 2  # make two of each
    random.shuffle(icons)

    # create the board data structure, with randomly placed icons
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for _ in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0]

        board.append(column)

    return board


def get_box_at_pixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = left_top_coords_of_box(boxx, boxy)
            box_rect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if box_rect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def left_top_coords_of_box(boxx, boxy):
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)


def split_into_groups_of(group_size, the_list):
    result = []
    for i in range(0, len(the_list), group_size):
        result.append(the_list[i:i + group_size])
    return result


def draw_icon(shape, colour, boxx, boxy):
    quarter = int(BOXSIZE * 0.25)  # syntactic sugar
    half = int(BOXSIZE * 0.5)  # syntactic sugar
    left, top = left_top_coords_of_box(boxx, boxy)  # get pixel coords from board coords

    # Draw the shapes
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, colour, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOUR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, colour, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, colour, (
        (left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, colour, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, colour, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, colour, (left, top + quarter, BOXSIZE, half))


def get_shape_and_colour(board, boxx, boxy):
    # shape stored in board[boxx][boxy][0]
    # colour stored in board[boxx][boxy][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]


def draw_box_covers(board, boxes, coverage):
    # draw boxes being covered / revealed. boxes is a list
    # of two item lists, which have the x and y spot of a box
    for box in boxes:
        left, top = left_top_coords_of_box(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOUR, (left, top, BOXSIZE, BOXSIZE))
        shape, colour = get_shape_and_colour(board, box[0], box[1])
        draw_icon(shape, colour, box[0], box[1])
        if coverage > 0:
            pygame.draw.rect(DISPLAYSURF, BOXCOLOUR,
                             (left, top, coverage, BOXSIZE))
        pygame.display.update()
        FPSCLOCK.tick(FPS)


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
                shape, colour = get_shape_and_colour(board, boxx, boxy)
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


def game_won_animation(board):
    # flash the background color when the player has won
    covered_boxes = generate_revealed_boxes_data(True)
    color1 = LIGHTBGCOLOUR
    color2 = BGCOLOUR

    for i in range(13):
        color1, color2 = color2, color1  # swap colors
        DISPLAYSURF.fill(color1)
        draw_board(board, covered_boxes)
        pygame.display.update()
        pygame.time.wait(300)


def has_won(revealed_boxes):
    # Returns True if all the boxes have been revealed, otherwise False
    for i in revealed_boxes:
        if False in i:
            return False  # return False if any boxes are covered.
    return True


if __name__ == "__main__":
    main()
