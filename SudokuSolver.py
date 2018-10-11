from Sudoku import Board
from Square import Square
from time import time


class SudokuSolver:
    """
    Properties created with the ``@property`` decorator should be documented
    in the property's getter method.

    Attributes:
        decisions (BoardDecision): list of decisions for guesses made.

    """

    def __init__(self, board=None):
        self.to_visit = set()
        self.open_squares = dict()
        self.decisions = list()
        self.solved = False
        if board is not None and type(board) is Board:
            self.board = board
        else:
            self.board = Board()
            self.board.initialize_breezy()
        for x in range(9):
            for y in range(9):
                if self.board.getPos(x,y).is_empty():
                    self.open_squares[x,y] = self.board.getPos(x,y)

    def block_check(self, x, y, num):
        if self.board.block_num(x, y, num):
            self.single_num(x, y)

    def get_intersecting(self, x, y):
        """
        Return a set of all empty squares that intersect with the selected square

        :param x:
        :type x: int
        :param y:
        :type y: int
        :return:
        :rtype: set
        """
        visit_set = set()
        quad_x = x // 3 * 3
        quad_y = y % 3 * 3

        for i in range(0, 9):
            self.add_on_empty(visit_set, x, i)   # col
            self.add_on_empty(visit_set, i, y)   #row
            self.add_on_empty(visit_set, quad_x + i // 3, quad_y + i % 3)    #blk

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
        single = list()
        # decisions = list()
        for i in range(9):
            for j in range(9):
                if self.board.is_empty(i, j):
                    single.append((i,j))

        print(single)

        while len(single) > 0:
            single.sort(key=lambda l: self.board.getPos(l[0], l[1]).open_count)

            item = single.pop(0)
            pos = self.board.getPos(item[0], item[1])
            if pos.has_single():
                try:
                    self.board.set_block(item[0], item[1], pos.get_single())
                except AssertionError:
                    self.reset_to_previous()

            else:
                self.decisions.append(BoardDecision(self.board.__repr__(), item, 0, pos.open_list()))
                try:
                    self.board.set_block(item[0], item[1], pos.open_list()[0])
                except IndexError:
                    self.solved = True
                    return

    def reset_to_previous(self):
        """
        :return:
        :rtype:
        """
        length = len(self.decisions)
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
        else:
            self.reset_to_previous()


class BoardDecision:
    def __init__(self, board, position, try_num, open_list):
        """
        Records previous states and decisions made

        :param board: board state represented as string
        :type board: str
        :param position:
        :type position: (int, int)
        :param try_num:
        :type try_num: int
        :param open_list:
        :type open_list: list of int
        """
        self.board = board
        self.pos = position
        self.try_num = try_num
        self.open_list = open_list


if __name__ == '__main__':
    total_time = time()
    solve = SudokuSolver()
    # solve.board.initialize_hard()
    solve.board.clear_board()
    solve.board.initialize_blocked()
    init_time = time() - total_time
    solve.trial_solve()
    total_time = time() - total_time
    print(solve.board)
    print(init_time)
    print(total_time)
    print(solve.solved)
    assert solve.board.is_solved() is solve.solved


    # visited = set()
    # solve.add_on_empty(visited, 0, 2)
    # lol = visited.pop()
    # print(lol)
