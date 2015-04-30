import sys
import pygame
from pygame.locals import *
import math

from CheckersGame import CheckerBoard, CheckerPiece, CheckerBoardLocation, Checkers


class PyGameCheckerBoard(CheckerBoard):
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    BOARD_COLOR = RED
    BOARD_BACKGROUND = BLACK

    SQUARE_SIZE_PX = 100
    BORDER_SIZE_PX = 5
    BOARD_SIZE_PX = (BORDER_SIZE_PX * 2) + (SQUARE_SIZE_PX * CheckerBoard.BOARD_SIZE)

    def __init__(self, game):
        super(PyGameCheckerBoard, self).__init__()
        self.game = game
        pygame.init()
        self.DISPLAYSURF = pygame.display.set_mode((PyGameCheckerBoard.BOARD_SIZE_PX, PyGameCheckerBoard.BOARD_SIZE_PX))
        # draw the green background
        self.DISPLAYSURF.fill(PyGameCheckerBoard.BOARD_BACKGROUND)

        pygame.display.set_caption('Checkers!')
        self.display()

    def create_piece(self, loc, player):
        return PyGameCheckerPiece(player, self)

    def display(self):
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                loc = CheckerBoardLocation(col, row)
                if self.is_square_playable(loc):
                    px = PyGameCheckerBoard.get_pixel_coords(loc)
                    pygame.draw.rect(self.DISPLAYSURF, PyGameCheckerBoard.BOARD_COLOR,
                                     (px, (PyGameCheckerBoard.SQUARE_SIZE_PX, PyGameCheckerBoard.SQUARE_SIZE_PX)))
                    piece = self.get_piece(loc)
                    if piece != self.EmptySpace:
                        piece.display(px)

        pygame.display.update()

    @staticmethod
    def get_pixel_coords(loc):
        start_x = PyGameCheckerBoard.BORDER_SIZE_PX + (loc.col * PyGameCheckerBoard.SQUARE_SIZE_PX)
        start_y = PyGameCheckerBoard.BORDER_SIZE_PX + (loc.row * PyGameCheckerBoard.SQUARE_SIZE_PX)
        return start_x, start_y

    def get_board_location(self, xy):
        loc = CheckerBoardLocation(0, 0)
        for col in range(self.BOARD_SIZE):
            current_square_start = PyGameCheckerBoard.BORDER_SIZE_PX + (PyGameCheckerBoard.SQUARE_SIZE_PX * col)
            next_square_start = PyGameCheckerBoard.BORDER_SIZE_PX + (PyGameCheckerBoard.SQUARE_SIZE_PX * (col + 1))
            if current_square_start <= xy[0] < next_square_start:
                loc.col = col
                break
        for row in range(self.BOARD_SIZE):
            current_square_start = PyGameCheckerBoard.BORDER_SIZE_PX + (PyGameCheckerBoard.SQUARE_SIZE_PX * row)
            next_square_start = PyGameCheckerBoard.BORDER_SIZE_PX + (PyGameCheckerBoard.SQUARE_SIZE_PX * (row + 1))
            if current_square_start <= xy[1] < next_square_start:
                loc.row = row
                break

        return loc


class PyGameCheckerPiece(CheckerPiece):
    RED = (128, 0, 0)
    BLACK = (32, 32, 32)
    GOLD = (255, 250, 180)
    KING_ICON = [(0, 0), (0, 10), (10, 10), (10, 0), (7.5, 4), (5, 0), (2.5, 4)]

    PIECE_RADIUS_PX = PyGameCheckerBoard.SQUARE_SIZE_PX * .4
    PIECE_OFFSET_PX = PyGameCheckerBoard.SQUARE_SIZE_PX / 2

    def display(self, coords):
        offset = self.PIECE_OFFSET_PX
        start_x = coords[0]
        start_y = coords[1]
        pygame.draw.circle(self.board.DISPLAYSURF, self.get_color(), (start_x + offset, start_y + offset),
                           int(self.PIECE_RADIUS_PX))
        if self.is_king():
            pygame.draw.lines(self.board.DISPLAYSURF, self.GOLD, True, self.get_relative_king_draw_points(coords))

    def get_relative_king_draw_points(self, coords):
        # Take the radius of the circle, and do some math
        inner_box_size = math.sqrt(((self.PIECE_RADIUS_PX * 2) ** 2) / 2)
        start_px = (self.board.SQUARE_SIZE_PX - inner_box_size) / 2
        draw_point_scale_factor = inner_box_size * .1
        return [(int((p[0] * draw_point_scale_factor) + start_px + coords[0]),
                 int((p[1] * draw_point_scale_factor) + start_px + coords[1])) for p in self.KING_ICON]


class PyGameCheckers(Checkers):
    def __init__(self):
        super(PyGameCheckers, self).__init__()
        self.moves = []

    def create_board(self):
        return PyGameCheckerBoard(self)

    def display(self):
        self.board.display()

    def get_move(self):
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                continue

            if event.type == MOUSEBUTTONUP and event.dict['button'] == 1:
                loc = self.board.get_board_location(event.dict['pos'])
                print loc
                if len(self.moves) > 1 and loc == self.moves[-1]:
                    try:
                        self.move_piece(self.moves)
                    except Exception as ex:
                        print ex.message
                    finally:
                        self.moves = []
                else:
                    self.moves.append(loc)

            if event.type == QUIT:
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    PyGameCheckers().play()

