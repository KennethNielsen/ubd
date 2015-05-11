"""Common components"""

from PyQt4.QtGui import QColor

COLOR_SCHEMES = {
    'green': {False: QColor('dark green'), True: QColor('lawn green')},
    'red': {False: QColor('dark red'), True: QColor('red')},
    'blue': {False: QColor('dark blue'), True: QColor('deep sky blue')},
}
