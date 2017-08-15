"""Common components"""

from collections import OrderedDict
from PyQt4.QtGui import QColor

COLOR_SCHEMES = OrderedDict((
    ('green', {False: QColor('dark green'), True: QColor('lawn green')}),
    ('red', {False: QColor('dark red'), True: QColor('red')}),
    ('blue', {False: QColor('dark blue'), True: QColor('deep sky blue')}),
))


class LabeledWidget:
    """A common implementation of a widget with a label"""

    def __init__(self, label):
        pass
