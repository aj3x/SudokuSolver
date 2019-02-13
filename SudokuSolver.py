from Sudoku import Board
from time import time


class SudokuSolver:
    """Creates a Sudoku board that can solve itself

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
                if self.board.getPos(x, y).is_empty():
                    self.open_squares[x, y] = self.board.getPos(x, y)

    def get_intersecting(self, x, y):
        """Return a set of all empty squares that intersect with the selected square

        Args:
            x (int): row index
            y (int): col index

        Returns:
            set[(int, int)]: Set of all empty squares that intersect with selected square
        """
        visit_set = set()
        quad_x = x // 3 * 3
        quad_y = y % 3 * 3

        for i in range(0, 9):
            self.add_on_empty(visit_set, x, i)   # col
            self.add_on_empty(visit_set, i, y)   # row
            q_x = quad_x + i // 3
            q_y = quad_y + i % 3
            self.add_on_empty(visit_set, q_x, q_y)    # blk

        return visit_set

    def add_on_empty(self, hash_set, x, y):
        """Adds position to hash set if the given position is empty

        Args:
            hash_set (set[(int, int)]):
            x (int): row index
            y (int): col index

        Returns:

        """
        if self.board.is_empty(x, y):
            hash_set.add((x, y))

    def trial_solve(self):
        """Solve the board using an efficient trial and error approach
        """
        single = list()
        for i in range(9):
            for j in range(9):
                if self.board.is_empty(i, j):
                    single.append((i, j))

        """
        1. sort open squares by least number of open possibilities
        2. go through and fill in all positions that only have one possibility 
        3. if no singles are left
            a)   
                 i) Save board before decision
                ii) Randomly select a number from the square with the smallest pool
               iii) Repeat steps 1-3
               
            b) If we end up in a state where the board is impossible
                go back a decision selecting something else 
        """
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
                # try guessing
                self.decisions.append(BoardDecision(self.board.__repr__(), item, 0, pos.open_list()))
                try:
                    self.board.set_block(item[0], item[1], pos.open_list()[0])
                except IndexError:
                    self.solved = True
                    return

    def reset_to_previous(self):
        """Resets board state to previous decision and tries another path.

        If all paths on that node have been tried move up another node
        and try from that point.
        """
        length = len(self.decisions)

        # if all paths have been tried return false
        if length is 0:
            self.solved = False
            return

        previous = self.decisions.pop()
        previous.try_num += 1

        # if we haven't tried all possibilities try the next one
        if previous.try_num < len(previous.open_list):
            self.board.clear_board()
            self.board.set_board(previous.board)
            self.board.set_block(previous.pos[0], previous.pos[1], previous.open_list[previous.try_num])
            self.decisions.append(previous)
            self.trial_solve()
        # tried all possibilities on this node: try the previous node
        else:
            self.reset_to_previous()

    def solve_set(self, arr):
        """

        Args:
            arr (str or list):

        Returns:
            (bool, str): Returns tuple of solvable, and error code
        """
        self.board.clear_board()
        self.board.set_board(arr)
        self.board.initialize_blocked()
        for i in range(9):
            for j in range(9):
                pos = self.board.getPos(i, j)
                solvable, errors = self.board.is_solvable()
                if pos.num == 0 == pos.open_count or not solvable:
                    return errors, "invalid board"
        self.trial_solve()
        return None, None


class BoardDecision:
    def __init__(self, board, position, try_num, open_list):
        """Records previous states and decision made

        Args:
            board (str): Board state represented as string
            position ((int, int)): Position of decision
            try_num (int): Number of times tried
            open_list (list of int): List of open numbers for the given square
        """
        self.board = board
        self.pos = position
        self.try_num = try_num
        self.open_list = open_list


if __name__ == '__main__':
    total_time = time()
    solve = SudokuSolver()
    solve.board.initialize_hard()
    init_time = time() - total_time
    solve.trial_solve()
    total_time = time() - total_time
    print(solve.board)
    print("Init time:\t%.5f" % init_time)
    print("Solve Time:\t%.5f" % (total_time-init_time))
    print("Total Time:\t%.5f" % total_time)
    print("Is Solved:\t" + str(solve.solved))
    assert solve.board.is_solved() is solve.solved
