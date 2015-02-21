#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Test of the idea of creating threaded methods for long running method
calls.

RESULT: Success! The two decorators implemented in threaded_methods.py make it
possible to have long running methods. Two variations have been implemented;
one for long running methods of which multiple instances can exist and one for
those where there mus be only one.

This program is adapted from the Zetcode tutorial:
http://zetcode.com/gui/pysidetutorial/ by Jan Bodnar.

"""

from __future__ import print_function
import sys
import time
import uuid
from PySide import QtGui, QtCore
from threaded_methods import live_forever, there_can_be_only_one


class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        
        qbtn = QtGui.QPushButton('Forever', self)
        qbtn.clicked.connect(self.forever)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 50)       

        qbtn = QtGui.QPushButton('Only one', self)
        qbtn.clicked.connect(self.only_one)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 80)       

        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Quit button')    
        self.show()

    @live_forever
    def forever(self):
        t = time.time()
        for n in range(3):
            time.sleep(1)
            print("Forever", t)
        print("Forever DONE")

    @there_can_be_only_one
    def only_one(self):
        print("Starting there can be only one")
        t = time.time()
        for n in range(5):
            time.sleep(1)
            print("Only one", t)
        print("Only one DONE")
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
