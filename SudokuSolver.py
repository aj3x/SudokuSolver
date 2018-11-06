from Sudoku import Board
from Square import Square
from time import time


class SudokuSolver:
    """
    Attributes:
        decisions (BoardDecision): list of decisions for guesses made.

    """

    def __init__(self, board=None):
        self.decisions = list()
        self.solved = False

        if board is not None and type(board) is Board:
            self.board = board
        else:
            # Initialize easy board
            self.board = Board()
            self.board.initialize_easy()

    def get_intersecting(self, x, y):
        """
        Return a set of all empty squares that intersect with the selected square

        :param x: row index
        :type x: int
        :param y: column index
        :type y: int
        :return: Set of all empty squares that intersect with selected square
        :rtype: set
        """
        visit_set = set()
        quad_x = x // 3 * 3
        quad_y = y % 3 * 3

        for i in range(0, 9):
            self.add_on_empty(visit_set, x, i)   # col
            self.add_on_empty(visit_set, i, y)   # row
            self.add_on_empty(visit_set, quad_x + i // 3, quad_y + i % 3)    # blk

        return visit_set

    def add_on_empty(self, hash_set, x, y):
        """

        :param hash_set:
        :type hash_set: set
        :param x:
        :type x: int
        :param y:
        :type y: int
        :return:
        :rtype:
        """
        if self.board.is_empty(x, y):
            hash_set.add((x, y))

    def trial_solve(self):
        """
        Attempts to solve the board using trial and error while selecting squares
        that reduce the number of attempts needed. 

        :return:
        :rtype: None
        """
        empty_squares = list()
        for i in range(9):
            for j in range(9):
                if self.board.is_empty(i, j):
                    empty_squares.append((i, j))

        while len(empty_squares) > 0:
            # sort open squares by number of possibilities
            empty_squares.sort(key=lambda l: self.board.getPos(l[0], l[1]).open_count)

            square = empty_squares.pop(0)
            pos = self.board.getPos(square[0], square[1])
            if pos.has_single():
                try:
                    self.board.set_block(square[0], square[1], pos.get_single())
                except AssertionError:
                    # Catch assertions that would make board state invalid
                    self.reset_to_previous()

            else:
                # try guessing
                self.decisions.append(BoardDecision(self.board.__repr__(), square, 0, pos.open_list()))
                try:
                    self.board.set_block(square[0], square[1], pos.open_list()[0])
                except IndexError:
                    self.solved = True
                    return

    def reset_to_previous(self):
        """
        Resets board state to previous decision and tries another path.
        If all paths on that node have been tried move up another node
        and try from that point.

        :return:
        :rtype: None
        """
        length = len(self.decisions)

        # if all paths have been tried return false
        if length is 0:
            self.solved = False
            return
        previous = self.decisions.pop(length-1)
        previous.try_num += 1

        # if we haven't tried all possibilities try the next one
        if previous.try_num < len(previous.open_list):
            self.board.clear_board()
            self.board.set_board(previous.board)
            self.board.set_block(previous.pos[0], previous.pos[1], previous.open_list[previous.try_num])
            self.decisions.append(previous)
            self.trial_solve()
        # tried all possibilities on this node try the previous node
        else:
            self.reset_to_previous()


class BoardDecision:
    def __init__(self, board, position, try_num, open_list):
        """
        Records previous states and decisions made

        :param board: board state represented as string
        :type board: str
        :param position: indices of the square (x,y)
        :type position: (int, int)
        :param try_num: how many possibilites have been tried
        :type try_num: int
        :param open_list: list of possibilites
        :type open_list: list of int
        """
        self.board = board
        self.pos = position
        self.try_num = try_num
        self.open_list = open_list


if __name__ == '__main__':
    total_time = time()
    solve = SudokuSolver()
    solve.board.clear_board()
    solve.board.initialize_hard()
    init_time = time() - total_time
    solve.trial_solve()
    total_time = time() - total_time
    print(solve.board)
    print("Init Time: %5f" % init_time)
    print("Total Time: %5f" % total_time)
    print("Is solved:",solve.solved)
    assert solve.board.is_solved() is solve.solved

