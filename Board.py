
# import cgitb
# cgitb.enable()
#
# print("Content-Type: text/plain;charset=utf-8")
# print()
# print("Hello World!")
import heapq


class Square:
    blocked = [False for x in range(9)]
    blocked_count = 9
    num = 0

    def __repr__(self):
        str_r = ""
        if self.num == 0:
            str_r = "("
            first = True
            for i in range(0,9):
                if not self.blocked[i]:
                    if first:
                        first = False
                    else:
                        str_r += ","
                    str_r += str(i+1)
            str_r += ")"
        else:
            str_r = str(self.num)
        return str_r

    def has_single(self):
        return self.blocked_count == 1

    def get_single(self):
        return self.blocked_list().pop(0)

    def is_empty(self):
        return self.num == 0

    def blocked_list(self):
        """
        Returns a list of open numbers from 1-9

        :return: List of open numbers
        :rtype: list of int
        """
        block_list = list()

        for i in range(0, 9):
            if not self.blocked[i]:
                block_list.append(i+1)

        return block_list

    def set_num(self, number):
        """
        Sets number and removes blocked if not equal to zero

        :param number: number to replace
        :type number: int
        :return: True if number isn't 0
        :rtype: bool
        """
        self.num = number
        if number != 0:
            self.blocked = None
            self.blocked_count = 0
            return True
        return False

class Sudoku:
    board = [[Square() for x in range(9)] for y in range(9)]
    unfilled = 81
    move_list = list()

    def initialize_easy(self):
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

    def clear_board(self):
        arr = [
            [0,0,0, 0,0,0, 0,0,0],
            [0,0,0, 0,0,0, 0,0,0],
            [0,0,0, 0,0,0, 0,0,0],

            [0,0,0, 0,0,0, 0,0,0],
            [0,0,0, 0,0,0, 0,0,0],
            [0,0,0, 0,0,0, 0,0,0],

            [0,0,0, 0,0,0, 0,0,0],
            [0,0,0, 0,0,0, 0,0,0],
            [0,0,0, 0,0,0, 0,0,0],
        ]
        self.set_board(arr)

    def set_board(self, arr):
        self.unfilled = 81
        for i in range(0,9):
            for j in range(0,9):
                self.board[i][j].blocked = [0 for r in range(0,9)]
                self.setPos(i,j,arr[i][j])
        self.initialize_blocked()

    def initialize_blocked(self):
        for x in range(0,9):
            for y in range(0,9):
                # if a number is in the position
                if not self.is_empty(x, y):

                    self.board[x][y].blocked = None

                    num = self.board[x][y].num
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
            raise ValueError("Out of bounds: "+num)
        return str(num)

    def __repr__(self):
        full = ""
        for i in range(0, 9):
            for j in range(0, 9):
                full += self.num_print(self.board[i][j].num)
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

    def is_filled(self):
        return self.unfilled == 0

    def setPos(self, x, y, num):
        assert(self.board[x][y].num == 0)
        self.assert_not_blocked(x, y, num)
        if self.board[x][y].set_num(num):
            self.unfilled -= 1

    def getPos(self, x, y):
        return self.board[x][y]

    def pos_count(self, x, y):
        return self.board[x][y].blocked_count

    def is_empty(self, x, y):
        return self.board[x][y].is_empty()

    def has_single(self, x, y):
        return self.board[x][y].has_single()

    def block_num(self, x, y, num):
        """
        Blocks a number in empty squares from being used.

        :param x: row index
        :type x: int
        :param y: column index
        :type y: int
        :param num: num in range(1,9) to block
        :type num: int
        :return:
        :rtype: None
        """
        # Spot is empty
        if self.is_empty(x, y):
            if not self.board[x][y].blocked[num-1]:
                self.board[x][y].blocked_count -= 1
                self.board[x][y].blocked[num-1] = True

    def block_solve(self, x, y, num, first=False):
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

        # block number in this position
        self.block_num(x, y, num)
        if self.has_single(x, y) or first:
            self.single_num(x, y)
            # if only one number is left
            # call block_solve on intersecting squares
            quad_x = x//3*3
            quad_y = y//3*3

            for i in range(0, 9):
                self.block_solve(x, i, num)
                self.block_solve(i, y, num)
                self.block_solve(quad_x + i % 3, quad_y + i//3, num)

    def single_num(self, x, y):
        """
        Check if the position has a single number left

        :param x: row index
        :type x: int
        :param y: column index
        :type y: int
        :return:
        :rtype:
        """
        if self.has_single(x, y):
            num = self.getPos(x, y).get_single()
            self.set_solve(x, y, num)

    def assert_not_blocked(self, x, y, num):
        """

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
            assert(self.getPos(x,i).num != num)
            assert(self.getPos(i,y).num != num)
            assert(self.getPos(quad_x + i % 3, quad_y + i//3).num != num)

    def available(self, x, y):
        arr = []
        for i in range(10):
            arr.append(True)
        arr[0] = False
        quad_x = x//3 * 3
        quad_y = y//3 * 3

        for i in range(0, 9):
            arr[self.getPos(x, i)] = False
            arr[self.getPos(i, y)] = False
            arr[self.getPos(quad_x + i % 3, quad_y + i/3)] = False

        avail = list()
        for i in range(1, 10):
            if arr[i]:
                avail.append()

    def set_solve(self, x, y, num):
        if self.getPos(x, y).num != 0:
            raise ValueError("Space already filled")

        self.setPos(x, y, num)
        self.block_solve(x, y, num, first=True)

    def solve(self):
        for x in range(0, 9):
            for y in range(0, 9):
                if self.is_empty(x, y):
                    self.single_num(x, y)

    def is_solved(self):
        for i in range(0,9):
            col = [True for x in range(0,9)]
            row = [True for x in range(0,9)]
            blk = [True for x in range(0,9)]

            quad_x = i // 3 * 3
            quad_y = i % 3 * 3

            for j in range(0, 9):
                col_i = self.board[j][i].num-1
                row_i = self.board[i][j].num-1
                blk_i = self.board[quad_x + j//3][quad_y + j % 3].num-1

                if 0<col_i<8 and 0<row_i<8 and 0<blk_i<8:
                    col[col_i] = False
                    row[row_i] = False
                    blk[blk_i] = False
                else:
                    print("Empty space at", i, j)
                    return False

            for k in range(0,9):
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

class Fart:
    pos = (1,2)
    count = 9

    def __init__(self, open_spots):
        self.count = open_spots

    def __eq__(self, other):
        """

        :param other:
        :type other: Fart
        :return:
        :rtype:
        """
        return self.count == other.count

    def __gt__(self, other):
        """

        :param other:
        :type other: Fart
        :return:
        :rtype:
        """
        return self.count > other.count

    def __lt__(self, other):
        """

        :param other:
        :type other: Fart
        :return:
        :rtype:
        """
        return self.count < other.count

    def __str__(self):
        return str(self.pos) + ' ' + str(self.count)


if __name__ == '__main__':
    lolz = dict()
    lolz["1,4"] = Fart(4)
    lolz["1,1"] = Fart(1)
    lolz["1,2"] = Fart(2)
    lolz["1,3"] = Fart(3)
    lolz["2,3"] = Fart(2)
    lolz["2,1"] = Fart(1)
    lol = [lolz["1,4"],lolz["1,1"],lolz["1,2"],lolz["1,3"],lolz["2,3"],lolz["2,1"]]
    h = heapq.heapify(lol)

    lolz["1,4"] = Fart(0)
    print(lol.pop(0))
    print(lol.pop(0))
    print(lol.pop())
"""
else:
    game = Sudoku()
    # game.set_solve(0, 0, 5)
    # game.board[0][2].num = 7
    game.initialize_easy()

    print(game.is_solved())
    game.display()
    game.solve()
    # print(game.board[5][8].blocked)
    #
    game.display()
    # print(game.getPos(0, 0))
"""
