from Square import Square
import unittest


class Board:
    board = [[Square(x, y) for x in range(9)] for y in range(9)]
    move_list = list()

    def __init__(self):

        #: list of Square: Doc comment *before* attribute, with type specified
        self.board = [[Square(x, y) for x in range(9)] for y in range(9)]
        self.move_list = list()
        self.answer = None

    def __repr__(self):
        full = ""
        for i in range(9):
            for j in range(9):
                full += str(self.board[i][j].num)
        return full

    def __str__(self):
        full = "\n"
        for i in range(0, 9):
            r_str = ""
            for j in range(0, 9):
                if j % 3 == 0:
                    r_str += "|"
                else:
                    r_str += " "
                r_str += self.num_print(self.board[i][j].num)

            full += r_str+"|\n"
            if i % 3 == 2:
                full += "-------------------\n"
        return full

    def get_board(self):
        return [[self.board[y][x].num for x in range(9)] for y in range(9)]

    def initialize_breezy(self):
        self.clear_board()
        self.answer = [
            [3,9,8, 7,1,5, 4,2,6],
            [2,7,1, 4,3,6, 5,9,8],
            [5,4,6, 8,9,2, 1,3,7],

            [6,3,7, 1,5,4, 2,8,9],
            [1,2,4, 3,8,9, 6,7,5],
            [8,5,9, 2,6,7, 3,4,1],

            [4,6,2, 9,7,1, 8,5,3],
            [7,8,5, 6,4,3, 9,1,2],
            [9,1,3, 5,2,8, 7,6,4],
        ]
        arr = [
            [3,9,8, 7,1,5, 4,2,6],
            [2,7,1, 4,3,6, 0,0,8],
            [5,4,6, 8,9,2, 1,3,7],

            [6,3,7, 1,5,4, 2,8,9],
            [1,2,4, 3,8,9, 6,7,5],
            [8,5,9, 2,6,7, 3,4,1],

            [4,6,2, 9,7,1, 8,5,3],
            [7,8,5, 6,4,3, 0,1,2],
            [9,1,3, 5,2,8, 7,6,4],
        ]
        self.set_board(arr)

    def initialize_easy(self):
        self.clear_board()
        self.answer = [
            [3,9,8, 7,1,5, 4,2,6],
            [2,7,1, 4,3,6, 5,9,8],
            [5,4,6, 8,9,2, 1,3,7],

            [6,3,7, 1,5,4, 2,8,9],
            [1,2,4, 3,8,9, 6,7,5],
            [8,5,9, 2,6,7, 3,4,1],

            [4,6,2, 9,7,1, 8,5,3],
            [7,8,5, 6,4,3, 9,1,2],
            [9,1,3, 5,2,8, 7,6,4],
        ]
        arr = [
            [3,9,0, 0,0,0, 0,2,0],
            [2,7,0, 0,0,6, 0,9,8],
            [0,4,0, 8,9,0, 0,0,7],

            [0,0,7, 0,5,0, 0,0,9],
            [0,2,0, 0,8,0, 0,7,0],
            [8,0,0, 0,6,0, 3,0,0],

            [4,0,0, 0,7,1, 0,5,0],
            [7,8,0, 6,0,0, 0,1,2],
            [0,1,0, 0,0,0, 0,6,4],
        ]
        self.set_board(arr)

    def initialize_medium(self):
        arr = "020089703" \
              "000015008" \
              "900000000" \
              "090000300" \
              "307000201" \
              "004000060" \
              "000000006" \
              "800470000" \
              "501930080"
        self.clear_board()
        self.set_board(arr)

    def initialize_hard(self):
        self.clear_board()
        arr = "007400002" \
              "030090050" \
              "400008300" \
              "800007400" \
              "010080090" \
              "006100007" \
              "001500008" \
              "080030070" \
              "600002900"
        self.set_board(arr)

    def initialize_impossible(self):
        self.clear_board()
        arr = [
            [3,9,0, 4,0,0, 0,2,0],
            [2,7,0, 0,0,6, 0,9,8],
            [0,4,0, 8,9,0, 0,0,7],

            [0,0,7, 0,5,0, 0,0,9],
            [0,2,0, 0,8,0, 0,7,0],
            [8,0,0, 0,6,0, 3,0,0],

            [4,0,0, 0,7,1, 0,5,0],
            [7,8,0, 6,0,0, 0,1,2],
            [0,1,0, 0,0,0, 0,6,4],
        ]
        self.set_board(arr)

    def clear_board(self):
        self.board = [[Square(x, y) for x in range(9)] for y in range(9)]

    def set_board(self, arr):
        if type(arr) == list:
            for i in range(9):
                for j in range(9):
                    self.board[i][j].reset_open()
                    self.setPos(i, j, arr[i][j])
        elif type(arr) == str:
            for i in range(9):
                for j in range(9):
                    self.board[i][j].reset_open()
                    self.setPos(i, j, int(arr[i*9+j]))
        self.initialize_blocked()

    def initialize_blocked(self):
        """
        Sets blocked positions from input board
        :return:
        :rtype: None
        """
        for x in range(9):
            for y in range(9):
                # if a number is in the position
                if not self.is_empty(x, y):

                    self.board[x][y].open = None

                    self.block_intersecting(x, y, self.getPos(x, y).num)

    def block_intersecting(self, x, y, num):
        quad_x = x//3*3
        quad_y = y//3*3

        for i in range(0, 9):
            self.block_num(x, i, num)
            self.block_num(i, y, num)
            self.block_num(quad_x + i % 3, quad_y + i//3, num)

    @staticmethod
    def num_print(num):
        """
        Returns display num

        :param num: int to be displayed
        :type num: int
        :return: display
        :rtype: string
        """
        if num == 0:
            return "_"
        if num > 9 or num < 0:
            raise ValueError("Out of bounds: "+str(num))
        return str(num)

    def display(self):
        """
        Prints Sudoku to console

        :return:
        :rtype: None
        """
        print("")
        for i in range(0, 9):
            r_str = ""
            for j in range(0, 9):
                if j % 3 == 0:
                    r_str += "|"
                else:
                    r_str += " "
                r_str += self.num_print(self.board[i][j].num)

            print(r_str+"|")
            if i % 3 == 2:
                print("-------------------")
            # print("+-+-+-+-+-+-+-+-+-+")

    def setPos(self, x, y, num):
        assert(self.is_empty(x, y))
        # self.assert_not_blocked(x, y, num)
        self.board[x][y].set_num(num)

    def getPos(self, x, y):
        return self.board[x][y]

    def pos_count(self, x, y):
        return self.board[x][y].open_count

    def is_empty(self, x, y):
        return self.board[x][y].is_empty()

    def has_single(self, x, y):
        return self.board[x][y].has_single()

    def block_num(self, x, y, num):
        """
        Blocks a number in empty squares from being used.
        Returns true if number changed.

        :param x: row index
        :type x: int
        :param y: column index
        :type y: int
        :param num: num in range(1,9) to block
        :type num: int
        :return: True if number changed
        :rtype: bool
        """
        if self.is_empty(x, y):
            if self.board[x][y].is_open(num):
                self.board[x][y].block_num(num)
                return True
        return False

    def set_block(self, x, y, num):
        """
        Sets position and blocks intersecting positions

        :param x: row index
        :type x: int
        :param y: col index
        :type y: int
        :param num: number
        :type num: int
        :return:
        :rtype: None
        """
        self.setPos(x, y, num)
        self.block_intersecting(x, y, num)

    def assert_not_blocked(self, x, y, num):
        """
        Asserts that position can contain that number

        :param x: row index
        :type x: int
        :param y: column index
        :type y: int
        :param num: number in square
        :type num: int
        :return: True if there are no intersecting numbers
        :rtype: bool
        """
        if num == 0:
            return

        quad_x = x//3*3
        quad_y = y//3*3
        for i in range(0,9):
            assert(self.getPos(x, i).num != num)
            assert(self.getPos(i, y).num != num)
            assert(self.getPos(quad_x + i % 3, quad_y + i//3).num != num)

    ERRORS_COL = 1
    ERRORS_ROW = 2
    ERRORS_BLK = 4

    def is_solvable(self):
        solvable = True
        errors = dict()
        for i in range(9):
            col = [True for x in range(9)]
            row = [True for x in range(9)]
            blk = [True for x in range(9)]

            quad_x = i // 3 * 3
            quad_y = i % 3 * 3

            for j in range(0, 9):
                col_i = self.board[j][i].num-1
                row_i = self.board[i][j].num-1
                blk_i = self.board[quad_x + j//3][quad_y + j % 3].num-1

                if col_i != -1:
                    if col[col_i]:
                        col[col_i] = False
                    else:
                        errors[j, i] = self.ERRORS_COL
                        # print("Duplicate at", j, i)
                        solvable = False

                if row_i != -1:
                    if row[row_i] is True:
                        row[row_i] = False
                    else:
                        errors[i, j] = self.ERRORS_ROW
                        # print("Duplicate at", i, j)
                        solvable = False

                if blk_i != -1:
                    if blk[blk_i] is True:
                        blk[blk_i] = False
                    else:
                        qx = quad_x + j // 3
                        qy = quad_y + j % 3
                        errors[qx, qy] = self.ERRORS_BLK
                        # print("Duplicate at", qx, qy)
                        solvable = False

            # for k in range(0, 9):
            #     if col[k] or row[k] or blk[k]:
            #         if col[k]:
            #             out = "column"
            #         elif row[k]:
            #             out = "row"
            #         else:
            #             out = "block"
            #         print("Fault in", out, i)
            #         return False
            return solvable, errors

    def is_solved(self):
        for i in range(0,9):
            col = [True for x in range(9)]
            row = [True for x in range(9)]
            blk = [True for x in range(9)]

            quad_x = i // 3 * 3
            quad_y = i % 3 * 3

            for j in range(0, 9):
                col_i = self.board[j][i].num-1
                row_i = self.board[i][j].num-1
                blk_i = self.board[quad_x + j//3][quad_y + j % 3].num-1

                if 0 <= col_i < 9:
                    col[col_i] = False
                else:
                    print("Empty space at", j, i)
                    return False

                if 0 <= row_i < 9:
                    row[row_i] = False
                else:
                    print("Empty space at", i, j)
                    return False

                if 0 <= blk_i < 9:
                    blk[blk_i] = False
                else:
                    print("Empty space at", quad_x + j//3, quad_y + j % 3)
                    return False

            for k in range(0, 9):
                if col[k] or row[k] or blk[k]:
                    if col[k]:
                        out = "column"
                    elif row[k]:
                        out = "row"
                    else:
                        out = "block"
                    print("Fault in", out, i)
                    return False
        return True

    # def list_errors(self, arr):
    #     errors = list()
    #     for i in range(9):
    #         col = dict()
    #         row = dict()
    #         blk = dict()
    #
    #         quad_x = i // 3 * 3
    #         quad_y = i % 3 * 3
    #
    #         for j in range(9):
    #             qx_i = quad_x + j//3
    #             qy_i = quad_y + j % 3
    #             col_i = self.arr[j][i]-1
    #             row_i = self.arr[i][j]-1
    #             blk_i = self.arr[qx_i][qy_i]-1
    #
    #             if col_i in col:







    @staticmethod
    def intersect_set(x, y):
        """

        :param x:
        :type x: int
        :param y:
        :type y: int
        :return:
        :rtype: set of (int,int)
        """
        r_set = set()
        quad_x = x//3*3
        quad_y = y//3*3

        for i in range(9):
            r_set.append(x, i)
            r_set.append(i, y)
            r_set.append(quad_x + i % 3, quad_y + i//3)

        r_set.discard(x, y)
        return r_set


class TestSudokuMethods(unittest.TestCase):
    def test_board_creation(self):
        b = Board()
        b.initialize_breezy()
        self.assertFalse(b.is_solved())
        arr = b.answer
        b = Board()
        b.set_board(arr)
        self.assertTrue(b.is_solved())

        b = Board()
        b.initialize_easy()
        self.assertFalse(b.is_solved())
        arr = b.answer
        b = Board()
        b.set_board(arr)
        self.assertTrue(b.is_solved())

    ALL_OPEN = list([1, 2, 3, 4, 5, 6, 7, 8, 9])
    MISSING_ONE = list([2, 3, 4, 5, 6, 7, 8, 9])

    def test_block_position(self):
        b = Board()

        self.assertEqual(b.getPos(0, 0).open_list(), self.ALL_OPEN)
        self.assertEqual(b.getPos(0, 0).open, [True, True, True, True, True, True, True, True, True])
        b.set_block(0, 0, 1)
        for i in range(9):
            for j in range(9):
                if i is 0 and j is 0:
                    assert_arr = None
                    assert_list = list()
                elif i is 0 or j is 0 or (0 <= i < 3 and 0 <= j < 3):
                    assert_arr = [False, True, True, True, True, True, True, True, True]
                    assert_list = self.MISSING_ONE
                else:
                    assert_arr = [True, True, True, True, True, True, True, True, True]
                    assert_list = self.ALL_OPEN

                self.assertEqual(b.getPos(i, j).open, assert_arr, str(i)+","+str(j))
                self.assertEqual(b.getPos(i, j).open_list(), assert_list, str(i)+","+str(j))
        b.set_block(8, 8, 9)
        self.assertEqual(b.getPos(0, 8).open_list(), list([2,3,4,5,6,7,8]))
        self.assertEqual(b.getPos(1, 8).open_list(), list([1,2,3,4,5,6,7,8]))

    def test_set_board(self):
        b = Board()
        b.initialize_breezy()
        b.display()
        self.assertEqual(b.getPos(0, 0).open_list(), list())
        self.assertEqual(b.getPos(0, 0).open_count, 0)

        self.assertEqual(b.getPos(1, 6).open_list(), list([5, 9]))
        self.assertEqual(b.getPos(1, 6).open_count, 2)

        self.assertEqual(b.getPos(1, 7).open_list(), list([9]))
        self.assertEqual(b.getPos(1, 7).open_count, 1)

        self.assertEqual(b.getPos(7, 6).open_list(), list([9]))
        self.assertEqual(b.getPos(7, 6).open_count, 1)

        b.set_block(1, 7, 9)
        self.assertFalse(b.is_solved())
        self.assertEqual(b.getPos(1, 6).open_list(), list([5]))
        self.assertEqual(b.getPos(1, 7).open_list(), list([]))
        self.assertEqual(b.getPos(7, 6).open_list(), list([9]))
        b.set_block(1, 6, 5)
        self.assertFalse(b.is_solved())
        self.assertEqual(b.getPos(1, 6).open_list(), list([]))
        self.assertEqual(b.getPos(1, 7).open_list(), list([]))
        self.assertEqual(b.getPos(7, 6).open_list(), list([9]))
        b.set_block(7, 6, 9)
        self.assertTrue(b.is_solved())
        self.assertEqual(b.getPos(1, 6).open_list(), list([]))
        self.assertEqual(b.getPos(1, 7).open_list(), list([]))
        self.assertEqual(b.getPos(7, 6).open_list(), list([]))


if __name__ == '__main__':
    unittest.TestCase()

    game = Board()
    game.initialize_easy()

    print(game.is_solved())
    game.display()

