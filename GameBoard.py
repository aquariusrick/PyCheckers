class OutOfBoundsException(Exception):
    pass


class Board:
    NO_PLAYER = None

    def __init__(self, cols, rows):
        self._board = []
        self._cols = cols
        self._rows = rows
        for i in range(rows):
            self._board.append([Board.NO_PLAYER] * cols)

    def set_piece(self, col, row, player):
        if 0 <= col < self._cols and 0 <= row < self._rows:
            self._board[row][col] = player
        else:
            raise OutOfBoundsException("Outside play area")

    def get_piece(self, col, row):
        if 0 <= col < self._cols and 0 <= row < self._rows:
            return self._board[row][col]
        else:
            return Board.NO_PLAYER

