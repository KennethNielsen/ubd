"""This module contains various utility functions, primarily for use during
development
"""

from kivy.graphics import Color, Rectangle
from kivy.logger import Logger

colors = []
RECT = {}


def myprint(to_print):
    Logger.info('###' + str(to_print))

def show(widget, color=(1, 0, 0)):
    global RECT
    col = color + tuple([0.6])
    #widget.canvas.add(Color(1, 0, 0, 0.6))
    widget.canvas.add(Color(*col))
    RECT[widget] = Rectangle(size=widget.size, pos=widget.pos)
    widget.canvas.add(RECT[widget])
    widget.bind(pos=_on_pos, size=_on_size)

def _on_pos(instance, value):
    RECT[instance].pos = value

def _on_size(instance, value):
    RECT[instance].size = value
