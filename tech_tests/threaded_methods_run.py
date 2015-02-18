#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Test of the idea of creating threaded methods for long running method
calls

This program is adapted from the Zetcode tutorial:
http://zetcode.com/gui/pysidetutorial/ by Jan Bodnar.
"""

from __future__ import print_function
import sys
import time
import uuid
from PySide import QtGui, QtCore
from threaded_methods import live_forever


class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        
        qbtn = QtGui.QPushButton('Quit', self)
        qbtn.clicked.connect(self.shjj)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 50)       
        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Quit button')    
        self.show()

    @live_forever
    def shjj(self):
        t = time.time()
        for n in range(10):
            time.sleep(1)
            print(t)
        print("DONE")
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
