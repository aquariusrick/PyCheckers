from CheckersGame import Checkers, CheckerBoard, CheckerPiece, CheckerBoardLocation


class ConsoleCheckerBoard(CheckerBoard):
    EmptySpace = ' '
    INVALID_SPACE = 'X'

    def display(self):
        print " ".join([" "] + [str(item) for item in range(self.BOARD_SIZE)])

        ctr = 0
        output = []
        for row in range(self.BOARD_SIZE):
            l = [str(ctr)] + [str(self.get_piece(CheckerBoardLocation(col, row))) for col in range(self.BOARD_SIZE)]
            output.append(" ".join(l))
            ctr += 1

        print "\n".join(output)

    def create_piece(self, loc, player):
        return ConsoleCheckerPiece(player, self)


class ConsoleCheckerPiece(CheckerPiece):
    RED = 'r'
    BLACK = 'b'

    def display(self):
        if self.is_king():
            return str(self.get_color()).upper()
        else:
            return str(self.get_color()).lower()

    def __str__(self):
        return self.display()


class ConsoleCheckers(Checkers):
    def create_board(self):
        return ConsoleCheckerBoard()

    def display(self):
        print ("Awaiting Player : %s" % self.current_player.name)
        self.board.display()

    def get_move(self):
        move_list = []

        moves = raw_input("What is your move Player %s? " % self.current_player.name)
        unparsed = moves.split('-')
        for m in unparsed:
            move = m.split('.')
            move_list.append(CheckerBoardLocation(int(move[0]), int(move[1])))

        try:
            self.move_piece(move_list)
        except Exception as ex:
            print ex.message

    @staticmethod
    def is_square_playable(loc):
        return (loc.col + loc.row) % 2 == 0


if __name__ == '__main__':
    ConsoleCheckers().play()