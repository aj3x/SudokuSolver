import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from SudokuSolver import SudokuSolver
import Sudoku


class SudokuWidget(QtWidgets.QWidget):
    boardText = ""
    valueChanged = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        self.solver = SudokuSolver()
        QWidget.__init__(self, parent)
        self.errors = dict()

        gbox = QGridLayout()


        c1 = QGraphicsView()
        color = QtGui.QColor(0)
        color.setBlue(255)
        gradient = QtGui.QRadialGradient(0, 0, 10)
        gradient.setSpread(QtGui.QGradient.RepeatSpread)
        c1.setForegroundBrush(color)

        c1.setPalette(QtGui.QPalette(QtGui.QColor(250, 250, 200)))
        c1.setAutoFillBackground(True)

        enter = QPushButton("Solve")
        enter.setMaximumHeight(40)
        enter.clicked.connect(self.solve)

        clear = QPushButton("Clear")
        clear.setMaximumHeight(40)
        clear.clicked.connect(self.clear)

        self.label = QLabel()

        self.squares = SquareWidget()
        gbox.addWidget(self.squares, 0, 0)
        hbox = QHBoxLayout()
        gbox.addWidget(self.label, 1, 0)
        hbox.addWidget(clear)
        hbox.addWidget(enter)
        gbox.addLayout(hbox, 2, 0, alignment=Qt.AlignRight)

        self.setLayout(gbox)

    def clear(self):
        self.squares.arr = [[0 for x in range(9)]for y in range(9)]
        self.squares.update()

    def solve(self):
        err_dict, err_str = self.solver.solve_set(self.squares.getArrStr())
        self.squares.arr = self.solver.board.get_board()

        ltext = ""
        if err_dict is not None:
            err = err_dict.popitem()
            if err[1] == Sudoku.Board.ERRORS_BLK:
                ltext = "Block"
            elif err[1] == Sudoku.Board.ERRORS_ROW:
                ltext = "Row"
            elif err[1] == Sudoku.Board.ERRORS_COL:
                ltext = "Col"
            ltext += " error at " + str(err[0])

        self.label.setText(ltext)
        self.squares.update()


class SquareWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.arr = [[0 for x in range(9)] for y in range(9)]
        self.intersect = dict()


        self.posx = 1
        self.posy = 1
        self.selectedx = -1
        self.selectedy = -1

        # box = QTextEdit()
        self.setPalette(QtGui.QPalette(QtGui.QColor(250, 250, 200)))
        self.setAutoFillBackground(True)
        # self.newTarget()
        self.setMouseTracking(True)
        self.setMaximumHeight(800)
        self.setFocusPolicy(Qt.StrongFocus)

    def paintBox(self, painter):
        """

        :param painter:
        :type painter: QtGui.QPainter
        :param x:
        :type x: int
        :param y:
        :type y: int
        :return:
        :rtype:
        """
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.blue)

        width = (self.width())//9
        height = (self.height())//9

        font = QtGui.QFont()
        font.setPixelSize(48)
        font.setFamily("Helvetica")
        painter.setFont(font)
        pen = QtGui.QPen()
        pen.setStyle(Qt.DotLine)
        painter.setPen(pen)

        painter.translate(0, 0)
        for x in range(9):
            for y in range(9):
                if x == self.selectedx and y == self.selectedy:
                    painter.setBrush(Qt.green)
                elif self.posx // width == x and self.posy // height == y:
                    painter.setBrush(Qt.lightGray)
                else:
                    painter.setBrush(Qt.gray)

                offset_x = 1
                offset_y = 1

                if x % 3 == 2:
                    offset_x = 3

                if y % 3 == 2:
                    offset_y = 3

                rect = QtCore.QRectF(x * width + offset_x//2, y * height+offset_y//2,
                                     width - 2*offset_x, height - 2*offset_y)
                painter.drawRect(rect)

                painter.setBrush(Qt.black)
                painter.drawText(x*width+8, y*height-10, width,height+10,0, self.getStrPos(y, x))

    def getStrPos(self, x, y):
        return str(self.arr[x][y]).strip("0")

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        self.paintBox(painter)

    def sizeHint(self):
        return QtCore.QSize(400, 400)

    def mouseMoveEvent(self, event):
        pos = event.pos()

        self.posx = pos.x()
        self.posy = pos.y()
        self.update()

    def mousePressEvent(self, event):
        width = self.width()/9
        height = self.height()/9

        self.selectedx = int(event.pos().x()//width)
        self.selectedy = int(event.pos().y()//height)

        self.update()

    def keyPressEvent(self, event):
        """

        :param event:
        :type event: QtGui.QKeyEvent
        :return:
        :rtype:
        """
        num = -1
        key = event.key()
        if key == Qt.Key_Space:
            num = 0
        elif key == Qt.Key_Backspace or key == Qt.Key_Delete:
            self.setCurPos(0)
        elif key == Qt.Key_Left:
            self.selectedx = (self.selectedx - 1) % 9
        elif key == Qt.Key_Right:
            self.selectedx = (self.selectedx + 1) % 9
        elif key == Qt.Key_Up:
            self.selectedy = (self.selectedy - 1) % 9
        elif key == Qt.Key_Down:
            self.selectedy = (self.selectedy + 1) % 9
        else:
            num = event.key() - 48

        if 0 <= num < 10:
            self.setCurPos(num)
            self.addPos()

        self.update()

    def setCurPos(self, num):
        if self.in_range(self.selectedx) and self.in_range(self.selectedy):
            self.arr[self.selectedy][self.selectedx] = num

            # TODO: Show numbers that are error on type
            # for (x, y) in Sudoku.Board.intersect_set(self.selectedx, self.selectedy):
            #     if self.arr[x][y] == num:
            #         if self.selectedx == x:
            #             code = 0
            #         elif self.selectedy == y:
            #             code = 1
            #         else:
            #             code = 2
            #


    def in_range(self, num):
        return 0 <= num < 10

    def addPos(self):
        self.selectedx = self.selectedx + 1
        if self.selectedx is 9:
            self.selectedx = 0
            self.selectedy = (self.selectedy + 1) % 9

    def getArrStr(self):
        r_str = ""
        for i in range(9):
            for j in range(9):
                if 9 < self.arr[i][j] < 0:
                    print("Number out of bounds")
                    r_str += "0"
                else:
                    r_str += str(self.arr[i][j])
        return r_str


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = SudokuWidget()
    widget.setWindowTitle("Sudoku Solver")
    icon = QtGui.QIcon("9.png")
    widget.setWindowIcon(icon)
    widget.show()

    sys.exit(app.exec_())
