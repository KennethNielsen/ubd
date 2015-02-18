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
THREADS_SINGLE = {}


def clean_up_threads():
    """Remove finished threads"""
    print("Clean up thread")
    for key, value in list(THREADS.items()):
        if value.isFinished():
            print("Removing", value)
            THREADS.pop(key)
    print("Threads now contain", THREADS)


def live_forever(func):
    """Thread decorator

    Spawns a thread for the method it decorates

    """

    class MyThread(QtCore.QThread):
        """Mythread"""

        def run(self):
            func(*self._func_args, **self._func_kwargs)
            clean_up_threads()

        def start(self, *args, **kwargs):
            self._func_args = args
            self._func_kwargs = kwargs
            super(MyThread, self).start()

    def new_func(*args, **kwargs):
        """New func"""
        # Clean up THREADS
        clean_up_threads()

        mythread = MyThread()
        uid = uuid.uuid4()
        THREADS[uid] = mythread
        mythread.start(*args, **kwargs)

    return new_func


def there_can_be_only_one(func):
    """Thread decorator

    Spawns a thread for the method it decorates, but makes sure that
    only one thread is spawned for each method

    """

    class MyThread(QtCore.QThread):
        """Mythread"""

        def run(self):
            func(*self._func_args, **self._func_kwargs)
            clean_up_threads()

        def start(self, *args, **kwargs):
            self._func_args = args
            self._func_kwargs = kwargs
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
