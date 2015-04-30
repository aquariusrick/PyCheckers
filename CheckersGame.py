import math
from enum import Enum, unique

import GameBoard


class InvalidCheckerMoveException(Exception):
    def __init__(self, message):
        self.message = message


class CheckerBoardLocation(object):
    def __init__(self, col, row):
        self.col = col
        self.row = row

    def __str__(self):
        return "(%s,%s)" % (self.col, self.row)

    def __eq__(self, other):
        return self.col == other.col and self.row == other.row

    def __ne__(self, other):
        return not self.__eq__(other)


class CheckerPiece(object):
    RED = ""
    BLACK = ""

    @unique
    class Rank(Enum):
        REGULAR = 1     # Regular pieces can only move forward
        KING = 2        # King pieces can move forward & backward

    @unique
    class Player(Enum):
        RED = 1
        BLACK = 2

    def __init__(self, player, board):
        self.player = player
        self.board = board
        self.rank = CheckerPiece.Rank.REGULAR

    def display(self):
        raise NotImplementedError()

    def __str__(self):
        return "%s %s" % (self.player.name, self.rank.name)

    def get_color(self):
        return self.RED if self.player == self.Player.RED else self.BLACK

    def make_king(self):
        self.rank = CheckerPiece.Rank.KING

    def is_king(self):
        return self.rank == CheckerPiece.Rank.KING

    def relative_to_player(self, location):
        if self.player == CheckerPiece.Player.BLACK:
            return CheckerBoardLocation(
                CheckerBoard.BOARD_SIZE - 1 - location.col,
                CheckerBoard.BOARD_SIZE - 1 - location.row)
        else:
            return location

    def move(self, *moves):
        move_ctr = int()
        is_piece_jumping = False
        was_kinged = False
        origin = moves[0]

        for dest in moves[1:]:
            move_ctr += 1
            try:
                if was_kinged:
                    raise InvalidCheckerMoveException("You cannot move after being Kinged!")

                if self.board.get_piece(dest) != self.board.EmptySpace:
                    raise InvalidCheckerMoveException("You cannot move there!")

                if not self.is_king() and self.relative_to_player(dest).row < self.relative_to_player(origin).row:
                    raise InvalidCheckerMoveException("This piece can only move forward!")

                jumped = self.is_jump(origin, dest)
                if move_ctr == 1:
                    is_piece_jumping = bool(jumped)
                else:
                    if not is_piece_jumping:
                        raise InvalidCheckerMoveException("Can only move once, unless you're jumping!")

                    if not bool(jumped):
                        raise InvalidCheckerMoveException("Once you start jumping, you must keep jumping!")

                if jumped:
                    piece = self.board.get_piece(jumped)
                    if piece != CheckerBoard.EmptySpace and piece.player != self.player:
                        self.board.set_piece(jumped, CheckerBoard.EmptySpace)
                    else:
                        raise InvalidCheckerMoveException("Can't jump piece at [%s]" % jumped)

                if self.relative_to_player(dest).row == (self.board.BOARD_SIZE - 1):
                    print "Player %s has been KINGED!" % self.player
                    self.make_king()
                    was_kinged = True

                self.board.set_piece(origin, CheckerBoard.EmptySpace)
                self.board.set_piece(dest, self)

            except GameBoard.OutOfBoundsException as ex:
                error = ("Move to [%s] is invalid: " % dest) + ex.message
                raise InvalidCheckerMoveException(error)

    @staticmethod
    def is_jump(start, end):
        col_diff = math.fabs(start.col - end.col)
        row_diff = math.fabs(start.row - end.row)

        if col_diff != row_diff:
            raise InvalidCheckerMoveException("You can only move diagonally!")

        if col_diff > 2:
            raise InvalidCheckerMoveException("You can't move that far!")

        if col_diff == 2 and row_diff == 2:
            return CheckerBoardLocation((start.col + end.col) / 2, (start.row + end.row) / 2)
        else:
            return False


class Checkers(object):
    def __init__(self):
        self.current_player = CheckerPiece.Player.BLACK
        self.turn_counter = 0
        self.board = self.create_board()

    def play(self):
        while True:
            self.display()
            self.get_move()

    def display(self):
        # This should be implemented on subclasses
        raise NotImplementedError()

    def get_move(self):
        # This should be implemented on subclasses
        raise NotImplementedError()

    def current_player(self):
        return self.current_player
    
    def create_board(self):
        return CheckerBoard()

    def get_owner(self, piece):
        if type(piece) is CheckerPiece:
            return piece.player
        else:
            return self.board.EmptySpace
    
    def opposite_player(self):
        return CheckerPiece.Player.RED if self.current_player == CheckerPiece.Player.BLACK \
            else CheckerPiece.Player.BLACK

    def move_piece(self, moves):
        if len(moves) < 2:
            raise InvalidCheckerMoveException("Please specify a new location!")

        origin = moves[0]
        piece = self.board.get_piece(origin)

        if piece.player == CheckerBoard.EmptySpace:
            raise InvalidCheckerMoveException("No player at that space!")

        if piece.player == self.opposite_player():
            raise InvalidCheckerMoveException("Incorrect Player!")

        piece.move(*moves)
        self.current_player = self.opposite_player()


class CheckerBoard(object):
    ROWS_OF_PIECES = 3
    BOARD_SIZE = 8
    EmptySpace = GameBoard.Board.NO_PLAYER
    INVALID_SPACE = 'X'
    
    def __init__(self):
        self.board = GameBoard.Board(CheckerBoard.BOARD_SIZE, CheckerBoard.BOARD_SIZE)
        self.place_starting_pieces()

    def create_piece(self, loc, player):
        piece = CheckerPiece(self, player)
        self.set_piece(loc, piece)

    def get_piece(self, loc):
        piece = self.board.get_piece(loc.col, loc.row)
        if not self.is_square_playable(loc):
            return self.INVALID_SPACE

        if isinstance(piece, CheckerPiece):
            return piece
        else:
            return self.EmptySpace

    def set_piece(self, loc, piece):
        try:
            self.board.set_piece(loc.col, loc.row, piece)
        except GameBoard.OutOfBoundsException as ex:
            raise InvalidCheckerMoveException(ex.message)

    def place_starting_pieces(self):
        board_size = self.BOARD_SIZE
        rows_of_pieces = self.ROWS_OF_PIECES

        red_rows = range(board_size)[:rows_of_pieces]
        black_rows = range(board_size)[-rows_of_pieces:]

        for col in xrange(board_size):
            for row in red_rows + black_rows:
                # Place them on alternating squares
                loc = CheckerBoardLocation(col, row)
                if self.is_square_playable(loc):
                    if row in red_rows:
                        piece = self.create_piece(loc, CheckerPiece.Player.RED)
                    else:
                        piece = self.create_piece(loc, CheckerPiece.Player.BLACK)

                    self.set_piece(loc, piece)

    @staticmethod
    def is_square_playable(loc):
        return (loc.col + loc.row) % 2 == 0
