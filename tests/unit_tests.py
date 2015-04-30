import unittest
from GameBoard import Board, OutOfBoundsException
from CheckersGame import CheckerBoard, CheckerPiece, CheckerBoardLocation, Checkers as CheckersGame, \
    InvalidCheckerMoveException


class GameBoardTests(unittest.TestCase):
    def setUp(self):
        self.rows = 8
        self.cols = 8
        self.board = Board(self.cols, self.rows)

    def testSettingPieces(self):
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                self.assertEqual(self.board.get_piece(col, row), Board.NO_PLAYER, msg="NO_PLAYER not set!")
                self.board.set_piece(col, row, "x")
                self.assertEqual(self.board.get_piece(col, row), "x",
                                 msg="Value not set on row: %s; col: %s" % (row, col))

    def testOutOfBounds(self):
        out_of_bounds = [
            (-1, 0),
            (self.cols + 1, 0),
            (0, -1),
            (0, self.rows + 1),
            (-1, -1),
            (self.cols + 1, self.rows + 1),
        ]
        for coord in out_of_bounds:
            self.assertRaises(OutOfBoundsException, self.board.set_piece, coord[0], coord[1], "x")


class CheckerBoardTests(unittest.TestCase):
    def setUp(self):
        self.board = CheckerBoard()

    def testCheckerBoardSetup(self):
        # Should have a usable 8x8 checkerboard.
        board = self.board
        board_size = CheckerBoard.BOARD_SIZE
        rows_of_pieces = CheckerBoard.ROWS_OF_PIECES
        self.assertEqual(board_size, 8, "Checkerboard is not 8x8!")
        self.assertEqual(rows_of_pieces, 3, "Checkerboard is not 8x8!")

        red_rows = range(board_size)[:rows_of_pieces]
        black_rows = range(board_size)[-rows_of_pieces:]

        for col in xrange(board_size):
            # Red pieces should be at the top
            for row in red_rows + black_rows:
                if (col+row) % 2 == 0:
                    board_location = CheckerBoardLocation(col, row)
                    piece = board.get_piece(board_location)
                    self.assertEqual(piece.rank, CheckerPiece.Rank.REGULAR,
                                     "Not a regular piece at location: %s" % board_location)

                    self.assertNotEqual(piece, CheckerBoard.EmptySpace)

                    if row in red_rows:
                        self.assertEqual(piece.player, CheckerPiece.Player.RED,
                                         "Red piece missing from location: %s" % board_location)
                    elif row in black_rows:
                        self.assertEqual(piece.player, CheckerPiece.Player.BLACK,
                                         "Black piece missing from location: %s" % board_location)


class CheckerPieceTests(unittest.TestCase):
    def setUp(self):
        self.red_piece = CheckerPiece(CheckerPiece.Player.RED)
        self.black_piece = CheckerPiece(CheckerPiece.Player.BLACK)

    def testPlayer(self):
        self.assertEqual(self.red_piece.player, CheckerPiece.Player.RED)
        self.assertEqual(self.black_piece.player, CheckerPiece.Player.BLACK)

    def testRank(self):
        self.assertEqual(self.red_piece.rank, CheckerPiece.Rank.REGULAR, "Red piece is not regular")
        self.assertEqual(self.black_piece.rank, CheckerPiece.Rank.REGULAR, "Black piece is not regular")

        self.red_piece.make_king()
        self.black_piece.make_king()

        self.assertEqual(self.red_piece.rank, CheckerPiece.Rank.KING, "Red piece is not a king")
        self.assertEqual(self.black_piece.rank, CheckerPiece.Rank.KING, "Black piece is not a king")


class CheckerGameTests(unittest.TestCase):
    def setUp(self):
        self.game = CheckersGame()

    def testValidMoves(self):
        start = CheckerBoardLocation(3, 5)
        end = CheckerBoardLocation(2, 4)
        piece = self.game.board.get_piece(start)
        self.game.move_piece((start, end))
        self.game.board.get_piece(end)

        self.assertIs(piece, self.game.board.get_piece(end))

    def testInvalidMoves(self):
        start = CheckerBoardLocation(3, 5)
        # Must have a start and end square.
        self.assertRaises(InvalidCheckerMoveException, self.game.move_piece, (start,))


        # Black piece can only move one space
        end = CheckerBoardLocation(1, 3)
        self.assertRaises(InvalidCheckerMoveException, self.game.move_piece, (start, end))

        # # Move a red piece in front a of a black piece
        # red_piece = self.game.board.get_piece(CheckerBoardLocation(4, 2))


if __name__ == '__main__':
    unittest.main()
