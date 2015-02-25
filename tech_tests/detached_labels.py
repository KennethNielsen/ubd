#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Test of selection of widgets, move and resize.

RESULT: Good. It seems feasable to implement. There are some design decisions
on the design of the builder that results from this.

This program is adapted from the Zetcode tutorial:
http://zetcode.com/gui/pysidetutorial/ by Jan Bodnar.

"""

import sys
from PySide import QtGui, QtCore
from PySide.QtCore import Qt

BORDERS = 5


class MovableMixin(object):

    def __init__(self, *args, **kwargs):
        super(MovableMixin, self).__init__(*args, **kwargs)
        self._offset = None
        self._draw_active = False
        self._pen = QtGui.QPen(QtGui.QColor(255, 0, 0, 127), 5)
        self._qp = QtGui.QPainter()

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._offset = e.pos()

    def mouseMoveEvent(self, e):
        if self._offset is not None:
            if self._offset.x() > self.width() - BORDERS:
                diff = e.pos() - self._offset
                self.resize(self.width() + diff.x(), self.height())
                self._offset = e.pos()
            else:
            #print(self.width())
                self.move(self.mapToParent(e.pos() - self._offset))

    def mouseReleaseEvent(self, e):
        if self._offset == e.pos():
            self.set_active(True)
            self.parentWidget().report_activated(self)            
        self._offset = None

    def set_active(self, state):
        self._draw_active = state
        self.update()

    def paintEvent(self, e):
        """Override paint event to draw active rectangle"""
        super(MovableMixin, self).paintEvent(e)
        if self._draw_active is True:
            # Draw red 'active' rectangle around widget
            self._qp.begin(self)
            self._qp.setPen(self._pen)
            width, height = self.size().toTuple()
            self._qp.drawRect(0, 0, width-1, height-1)
            self._qp.end()


class MovableLabel(MovableMixin, QtGui.QLabel):
    pass


class MovableButton(MovableMixin, QtGui.QPushButton):
    pass


class Example(QtGui.QWidget):
    
    def __init__(self):
        self._draw_active = False
        super(Example, self).__init__()
        self._offset = None
        self._present = None
        self._pen = QtGui.QPen(QtGui.QColor(255, 0, 0), 2)
        self._qp = QtGui.QPainter()
        self._last_selection_square = None
        self.widgets = []
        self.initUI()
        
    def initUI(self):
                
        #btn = QtGui.QPushButton('Button', self)
        #btn.setToolTip('This is a <b>QPushButton</b> widget')
        self.label = MovableLabel("My new label", parent=self)
        self.label.resize(self.label.sizeHint())
        self.label.move(50, 50)
        self.widgets.append(self.label)

        self.btn = MovableButton("My new button", parent=self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(50, 80)
        self.widgets.append(self.btn)
        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Tooltips')    
        self.show()

    def look_at_me(self):
        #self.btn.resize(-1, 100)
        print('Look at me')

    def report_activated(self, widget):
        print(widget, 'reports is active')
        for widget_in_list in self.widgets:
            if widget_in_list != widget:
                print('Deactive', widget_in_list)
                widget_in_list.set_active(False)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._offset = e.pos()        

    def mouseMoveEvent(self, e):
        if self._offset is not None:
            self._present = e.pos()
            self.update()

    def mouseReleaseEvent(self, e):
        self._offset = None
        if self._last_selection_square is not None:
            print('select', self._last_selection_square)
            self._last_selection_square = None
            self.update()

    def paintEvent(self, e):
        """Override paint event to draw active rectangle"""
        super(Example, self).paintEvent(e)
        if self._offset is not None:
            # Draw red 'active' selection rectangle
            self._qp.begin(self)
            self._qp.setPen(self._pen)
            pos = self._offset.toTuple()
            current = self._present.toTuple()
            args = [min(a, b) for a,b in zip(pos, current)]
            args += [abs(a - b) - 1 for a,b in zip(pos, current)]
            # Top left x, y and width height
            self._last_selection_square = args
            
            width, height = self.size().toTuple()
            self._qp.drawRect(*args)
            self._qp.end()
        

def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
