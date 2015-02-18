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


THREADS = {}


def clean_up_threads():
    """Remove finished threads"""
    print("Clean up thread")
    for key, value in list(THREADS.items()):
        if value.isFinished():
            print("Removing", value)
            THREADS.pop(key)
    print("Threads now contain", THREADS)


def thread_dec(func):
    """Thread decorator"""

    class MyThread(QtCore.QThread):
        """Mythread"""

        def run(self):
            #socket = QTcpSocket()
            # connect QTcpSocket's signals somewhere meaningful
            # ...
            #socket.connectToHost(hostName, portNumber)
            #self.exec_()
            #func(*ARGS[0], **ARGS[1])
            func(*self.___args, **self.___kwargs)
            clean_up_threads()

        def start(self, *args, **kwargs):
            self.___args = args
            self.___kwargs = kwargs
            super(MyThread, self).start()

    def new_func(*args, **kwargs):
        """New func"""
        # Clean up THREADS
        clean_up_threads()

        mythread = MyThread()
        uid = uuid.uuid1()
        THREADS[uid] = mythread
        mythread.start(*args, **kwargs)

    return new_func


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

    @thread_dec
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
