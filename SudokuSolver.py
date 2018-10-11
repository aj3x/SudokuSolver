from Sudoku import Board
from Square import Square
from time import time


class SudokuSolver():
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

    def solve(self):
        for x in range(0, 9):
            for y in range(0, 9):
                if self.board.is_empty(x, y):
                    self.single_num(x, y)
        self.board.display()

    def single_num(self, x, y):
        """
        Checks for block with single num then solves for intersecting blocks

        :param x: row index
        :type x: int
        :param y: column index
        :type y: int
        :return:
        :rtype: None
        """
        if self.board.has_single(x, y):
            num = self.board.getPos(x, y).get_single()
            self.set_solve(x, y, num)

    # On num change:
    # Check for changes on three rows, columns and single region

    def set_solve(self, x, y, num):
        if self.board.getPos(x, y).num != 0:
            raise ValueError("Space already filled")

        self.board.setPos(x, y, num)
        self.to_visit.discard((x, y))
        self.block_solve(x, y, num)

    def block_solve(self, x, y, num):
        """
        Iterates across blocking and finding naked numbers

        :param x: row index
        :type x: int
        :param y: column index
        :type y: int
        :param num: number for block range(1-9)
        :type num: int
        :param first: is initial block
        :type first: bool
        :return:
        :rtype: None
        """

        # if only one number is left
        # call block_solve on intersecting squares
        quad_x = x // 3 * 3
        quad_y = y // 3 * 3

        for i in range(0, 9):
            self.block_check(x, i, num)
            self.block_check(i, y, num)
            self.block_check(quad_x + i % 3, quad_y + i // 3, num)

    def block_check(self, x, y, num):
        if self.board.block_num(x, y, num):
            self.single_num(x, y)

    def hidden_single(self):
        self.block_function(start=0, square_func=lambda x: x.num * 2)
        # for i in range(9):
        #     row = [list() for x in range(9)]
        #     col = [list() for x in range(9)]
        #     blk = [list() for x in range(9)]
        #
        #     quad_x = i // 3 * 3
        #     quad_y = i % 3 * 3
        #
        #     for j in range(9):
        #         row_num = self.board.getPos(j,i)
        #         col_num = self.board.getPos(i,j)
        #         blk_num = self.board[quad_x + j//3][quad_y + j % 3].num-1

    def block_function(self, start=True, condition=False, accept_func=None, square_func=None):
        for i in range(0,9):
            col = [start for x in range(9)]
            row = [start for x in range(9)]
            blk = [start for x in range(9)]

            quad_x = i // 3 * 3
            quad_y = i % 3 * 3

            for j in range(0, 9):
                col_i = self.board.getPos(j, i)
                row_i = self.board.getPos(i, j)
                blk_i = self.board.getPos(quad_x + j//3, quad_y + j % 3)

                if square_func is not None:
                    print("does it work?", col_i, square_func(col_i))

                if condition and accept_func is not None:
                    print("Some code is incomplete")

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


    def check_and_solve(self, x, y):
        quad_x = x // 3 * 3
        quad_y = y % 3 * 3

        for i in range(0, 9):
            col = (x, i)
            row = (i, y)
            blk = (quad_x + i // 3, quad_y + i % 3)

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
            # for s in single:
            #     assert(self.board.getPos(s[0],s[1]).num == 0)

            # for s in single:
            #     print(self.board.getPos(s[0],s[1]).open_count)
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
                    print(self.board)

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
    solve.board.initialize_impossible()
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
