#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Test of Managed Widgets

RESULT: Success. It seems to work just fine and the idea of separating them
into .i and .o or input and output works well

This program is adapted from the Zetcode tutorial:
http://zetcode.com/gui/pysidetutorial/ by Jan Bodnar.

"""

import sys
from PySide import QtGui
from managed_base import UbdApp


class Example(UbdApp):
    """My fancy app"""

    def __init__(self):
        super(Example, self).__init__()

    def printer(self, value):
        """Multiply printer"""
        print "Myline set to:", value
        self.o.lineout = self.i.myline * self.i.myint


if __name__ == '__main__':
    APP = QtGui.QApplication(sys.argv)
    EX = Example()
    sys.exit(APP.exec_())
