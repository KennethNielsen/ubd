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
import threading
import Queue
from PySide import QtGui, QtCore


THREADS = {}
THREADS_SINGLE = {}


def clean_up_threads():
    """Remove finished forever threads"""
    print("Clean up forever threads")
    for key, value in list(THREADS.items()):
        if value.isFinished():
            print('Removing forever', key)
            THREADS.pop(key)
    print('Forever threads now contain', len(THREADS), 'threads')

    print("Clean up single threads")
    for key, value in list(THREADS_SINGLE.items()):
        if value.isFinished():
            print('Removing single', key)
            THREADS_SINGLE.pop(key)
    print('Single threads now contain', len(THREADS), 'threads')


def live_forever(func):
    """Thread decorator

    Spawns a thread for the method it decorates

    """
    class MyThread(QtCore.QThread):
        """Mythread"""

        def run(self):
            func(*self._func_args, **self._func_kwargs)
            THREADSTEWARD.enqueue_cleanup(clean_up_threads)

        def start(self, *args, **kwargs):
            self._func_args = args
            self._func_kwargs = kwargs
            super(MyThread, self).start()

    def new_func(*args, **kwargs):
        """New func"""
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
            THREADSTEWARD.enqueue_cleanup(clean_up_threads)

        def start(self, *args, **kwargs):
            self._func_args = args
            self._func_kwargs = kwargs
            super(MyThread, self).start()

    def new_func(*args, **kwargs):
        """New func"""
        func_id = id(func)
        if func_id in THREADS_SINGLE and THREADS_SINGLE[func_id].isRunning():
            print("THERE CAN BE ONLY ONE! Aborting")
            return

        mythread = MyThread()
        THREADS_SINGLE[func_id] = mythread
        mythread.start(*args, **kwargs)

    return new_func


class ThreadSteward(threading.Thread):

    def __init__(self):
        self.cleanup_queue = Queue.Queue()
        super(ThreadSteward, self).__init__()
        self.daemon = True

    def run(self):
        while True:
            cleanup_func = self.cleanup_queue.get()
            cleanup_func()

    def enqueue_cleanup(self, cleanup_type):
        self.cleanup_queue.put(cleanup_type)


THREADSTEWARD = ThreadSteward()
THREADSTEWARD.start()
