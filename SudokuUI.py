import sys
from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtWidgets import *
import SudokuSolver


class SudokuWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        hbox = QHBoxLayout()
        # hbox.addWidget(SquareWidget())
        text = QTextEdit()
        text23 = QLineEdit()
        text23.setValidator(QtGui.QIntValidator(0,9))
        text23.setFixedWidth(40)
        if text23.text()=="":
            print("yes")
        text.setLineWrapMode(3)
        text.setLineWrapColumnOrWidth(9)
        text.setFixedHeight(40)
        text.setTabChangesFocus(True)

        c1 = QGraphicsView()
        color = QtGui.QColor(0)
        color.setBlue(255)
        gradient = QtGui.QRadialGradient(0,0,10)
        gradient.setSpread(QtGui.QGradient.RepeatSpread)
        c1.setForegroundBrush(color)

        c1.setPalette(QtGui.QPalette(QtGui.QColor(250,250,200)))
        c1.setAutoFillBackground(True)
        # c1.

        enter = QPushButton("Enter")

        hbox.addWidget(c1)

        # machine = QtGui.
        s1 = QtCore.QState()
        s1.assignProperty(text, 'text', 'Outside')
        # text.keyPressEvent()
        text2 = QTextEdit()
        hbox.addWidget(text)
        hbox.addWidget(enter)
        hbox.addWidget(SquareWidget())

        self.setLayout(hbox)

class SquareWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.posx = 1
        self.posy = 1
        self.selectedx = -1
        self.selectedy = -1

        # box = QTextEdit()
        self.setPalette(QtGui.QPalette(QtGui.QColor(250, 250, 200)))
        self.setAutoFillBackground(True)
        # self.newTarget()
        self.setMouseTracking(True)

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
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.blue)

        width = (self.width())//9
        height = (self.height())//9




        # painter.save()
        painter.translate(0, 0)
        for x in range(9):
            for y in range(9):
                if x == self.selectedx and y == self.selectedy:
                    painter.setBrush(QtCore.Qt.darkRed)
                elif self.posx // width == x and self.posy // height == y:
                    painter.setBrush(QtCore.Qt.red)
                else:
                    painter.setBrush(QtCore.Qt.blue)
                offset_x = 1
                offset_y = 1

                if x % 2 == 0:
                    offset_x = 0

                if y % 2 == 0:
                    offset_y = 0

                painter.drawRect(QtCore.QRect(x * width + offset_x, y * height+offset_y,
                                              width - 2*offset_x, height - 2*offset_y))
        # painter.restore()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        self.paintBox(painter)

    def sizeHint(self):
        return QtCore.QSize(400, 400)

    def mouseMoveEvent(self, event):
        pos = event.pos()

        print("moved", pos.x(),pos.y())

        self.posx = pos.x()
        self.posy = pos.y()
        self.update()

    def mousePressEvent(self, event):
        print("pressed")

        width = self.width()/9
        height = self.height()/9

        self.selectedx = event.pos().x()//width
        self.selectedy = event.pos().y()//height

        self.update()

    def keyPressEvent(self, event):
        """

        :param event:
        :type event: QtGui.QKeyEvent
        :return:
        :rtype:
        """
        print("keyPressed")
        print(event.key())



if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    widget = SudokuWidget()
    widget.show()
    sys.exit(app.exec_())