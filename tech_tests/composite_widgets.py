#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Test of the mechanism for creating composite widgets

RESULT: NOT FAVORABLE. Probably not a good idea. The move and change code will
get to contain a lot of special cases. Look into keeping widget and label
seperate.

This program is adapted from the Zetcode tutorial:
http://zetcode.com/gui/pysidetutorial/ by Jan Bodnar.

"""

import sys
from PySide import QtGui, QtCore
from PySide.QtCore import Qt

BORDERS = 5


class LabeledButton(QtGui.QWidget):
    def __init__(self, parent, debug=False):
        super(LabeledButton, self).__init__(parent)

        # Init UI
        self.label = QtGui.QLabel('My button .................', self)
        self.button = QtGui.QPushButton('Look at me', self)
        vbox = QtGui.QVBoxLayout()
        vbox.setSpacing(BORDERS)
        vbox.setContentsMargins(*[BORDERS] * 4)
        vbox.addWidget(self.label)
        vbox.addWidget(self.button)
        self.setLayout(vbox)

        # In debug color widget backgrounds
        if debug:
            self._color_widget(self, (255, 0, 0, 50))
            self._color_widget(self.label, (0, 255, 0, 50))
            self._color_widget(self.button, (0, 255, 0, 50))

        # Bind
        self.bind(parent)

        self.mouse_press = None

    def bind(self, parent):
        self.button.clicked.connect(parent.look_at_me)

    def mouseReleaseEvent(self, e):
        #size = self.size()
        #size += QtCore.QSize(10, 0)
        #self.resize(size)
        if e.pos() == self.mouse_press:
            print('Clicked')

    def mousePressEvent(self, e):
        pos = e.pos()
        self.mouse_press_pos = pos

        if pos.x() <= BORDERS:
            self.mouse_os = 'left'

        if pos.x() >= self.width() - BORDERS:
            self.mouse_on = 'right'

    @staticmethod
    def _color_widget(widget, color):
        widget.setAutoFillBackground(True)
        palette = widget.palette()
        #palette.setColor(widget.backgroundRole(), color)
        palette.setColor(widget.backgroundRole(), QtGui.QColor(*color))
        widget.setPalette(palette)


class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        
    def initUI(self):
                
        #btn = QtGui.QPushButton('Button', self)
        #btn.setToolTip('This is a <b>QPushButton</b> widget')
        self.btn = LabeledButton(self, debug=True)
        #self.btn.resize(self.btn.sizeHint())
        self.btn.move(50, 50)
        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Tooltips')    
        self.show()

    def look_at_me(self):
        #self.btn.resize(-1, 100)
        print('Look at me')
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
