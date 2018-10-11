import unittest

# Constants
EMPTY = 0


class Square:
    open = [True for x in range(0, 9)]
    open_count = 9
    num = EMPTY

    def __init__(self, x, y):
        self.reset_open()
        self.open_count = 9
        self.num = EMPTY
        self.x = x
        self.y = y

    def __str__(self):
        if self.num == 0:
            str_r = "("
            first = True
            for i in range(0,9):
                if self.open[i]:
                    if first:
                        first = False
                    else:
                        str_r += ","
                    str_r += str(i+1)
            str_r += ")"
        else:
            str_r = str(self.num)
        return str_r

    def __repr__(self):
        return self.num

    @staticmethod
    def in_range(number):
        if 9 < number < 1:
            raise ValueError("Number must be in range(0,9) input: ", number)

    def has_single(self):
        return self.open_count == 1

    def get_single(self):
        if not self.has_single():
            raise AssertionError("Called on square with multiple open numbers")
        if len(self.open_list()) is not 1:
            raise ValueError("has_single returned true while the value was not 1:", len(self.open_list()))
        return self.open_list().pop(0)

    def is_empty(self):
        return self.num == 0

    def get_num(self):
        return self.num

    def open_list(self):
        """
        Returns a list of open numbers from 1-9

        :return: List of open numbers
        :rtype: list of int
        """
        num_list = list()

        if self.open is not None:
            for i in range(0, 9):
                if self.open[i]:
                    num_list.append(i+1)

        return num_list

    def reset_open(self):
        self.open = [True for x in range(0, 9)]

    def set_num(self, number):
        """
        Sets number and removes blocked if not equal to zero

        :param number: number to replace
        :type number: int
        :return: True if number isn't 0
        :rtype: bool
        """
        self.in_range(number)
        self.num = number
        if number != 0:
            self.open = None
            self.open_count = 0
            return True
        return False

    def is_open(self, number):
        self.in_range(number)
        return self.open[number-1]

    def block_num(self, number):
        """


        :param number: number in range 0
        :type number: int
        :return: True if value wasn't previously blocked
        :rtype: bool
        """
        self.in_range(number)
        if self.is_empty() and self.open[number-1]:
            self.open[number-1] = False
            self.open_count -= 1
            assert(self.open_count > 0)
            return True
        return False

    def intersect(self, other):
        """

        :param other:
        :type other: Square
        :return:
        :rtype: bool
        """
        return self.x == other.x or self.y == other.y or (self.get_region() == other.get_region())

    def get_region(self):
        """
        Return tuple of int from range(0,2)

        :return:
        :rtype: tuple of int
        """
        return self.x // 3, self.y // 3


class TestSquareMethods(unittest.TestCase):
    def test_init(self):
        s = Square(0, 0)
        self.assertEqual(s.is_empty(), True)
        self.assertEqual(s.has_single(), False)
        self.assertEqual(s.get_num(), 0)

    def test_set_num(self):
        s = Square(0, 0)

        s.set_num(0)
        self.assertEqual(s.is_empty(), True)
        self.assertEqual(s.has_single(), False)
        self.assertEqual(s.get_num(), 0)

        s.set_num(1)
        self.assertEqual(s.is_empty(), False)
        self.assertEqual(s.has_single(), False)
        self.assertEqual(s.get_num(), 1)

    def test_open_list(self):
        s = Square(0, 0)
        self.assertEqual(s.block_num(1), True)
        self.assertEqual(s.block_num(1), False)
        self.assertEqual(s.open, [False, True, True, True, True, True, True, True, True])
        self.assertEqual(s.has_single(), False)
        self.assertEqual(s.open_count, 8)

    def test_single(self):
        s = Square(0, 0)
        self.assertEqual(s.block_num(1), True)
        self.assertEqual(s.block_num(2), True)
        self.assertEqual(s.block_num(3), True)
        self.assertEqual(s.block_num(4), True)
        self.assertEqual(s.block_num(5), True)
        self.assertEqual(s.block_num(6), True)
        self.assertEqual(s.block_num(9), True)
        self.assertEqual(s.has_single(), False)
        self.assertEqual(s.open_count, 2)
        self.assertEqual(s.block_num(8), True)
        self.assertEqual(s.has_single(), True)
        self.assertEqual(s.open_count, 1)

    def test_intersect(self):
        a = Square(1, 1)
        b = Square(2, 2)
        c = Square(1, 1)
        d = Square(1, 6)
        e = Square(6, 1)
        f = Square(3, 3)
        self.assertEqual(a.get_region(), b.get_region(), c.get_region())
        self.assertTrue(a.intersect(b))
        self.assertTrue(a.intersect(d))
        self.assertTrue(a.intersect(e))

        self.assertFalse(f.intersect(a))
        self.assertFalse(f.intersect(b))
        self.assertFalse(f.intersect(c))
        self.assertFalse(f.intersect(d))
        self.assertFalse(f.intersect(e))


if __name__ == '__main__':
    unittest.main()
