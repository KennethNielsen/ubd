#!/usr/bin/env python
# pylint: disable=C0103

"""Boolean output widgets

This module implements the following boolean output widgets: LED
"""

from __future__ import print_function

from PyQt4.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt4.QtGui import QFrame, QPen, QPainter, QHBoxLayout
from PyQt4.QtGui import QWidget

from common import COLOR_SCHEMES


class LED(QFrame):
    """A LED boolean output"""

    border_width = 2
    edge_width = 2

    # Define stateChanged signal, which can be emitted with a boolean or no arguments
    stateChanged = pyqtSignal([bool], [])

    def __init__(self, parent=None, initial_state=False, color_scheme='green', debug=False):
        super(LED, self).__init__(parent)
        try:
            self.color_scheme = COLOR_SCHEMES[color_scheme]
        except KeyError:
            message = 'Invalid color scheme name. Valid values are: {}'
            raise ValueError(message.format(COLOR_SCHEMES.keys()))

        # Calculate the minimum size and set it
        minimum = (self.border_width + self.edge_width) * 2 + 1
        self.setMinimumSize(minimum, minimum)

        # Set the state of the widget on start up
        self._state = initial_state

        # Setup drawing
        self.qpainter = QPainter()
        self.pen = QPen(Qt.black, self.edge_width, Qt.SolidLine)

        if debug:
            self.setStyleSheet("background-color:red;")

        self.update()

    def state(self):
        """Return the boolean state"""
        return self._state

    @pyqtSlot(bool)
    @pyqtSlot(bool, bool)
    def setState(self, state, no_emit=False):
        """Set the boolean state"""
        self._state = state
        self.update()
        if not no_emit:
            self.stateChanged.emit(self._state)

    def paintEvent(self, _):
        """Redraw LED on paint event"""
        self.qpainter.begin(self)
        self.qpainter.setPen(self.pen)
        self.qpainter.setBrush(self.color_scheme[self._state])
        size = self.size()
        self.qpainter.drawEllipse(
            self.border_width,
            self.border_width,
            size.width() - 2 * self.border_width,
            size.height() - 2 * self.border_width)
        self.qpainter.end()


def main():
    """Elementary widget test"""
    import sys
    from PyQt4.QtGui import QApplication
    from PyQt4.QtCore import QTimer
    app = QApplication(sys.argv)

    class Example(QWidget):
        """Tester"""

        def __init__(self):
            super(Example, self).__init__()
            self.led = LED(color_scheme='green')
            self.led.stateChanged.connect(self.receive)
            self.led.stateChanged.connect(self.receive_with_args)
            hbox = QHBoxLayout()
            hbox.addWidget(self.led)
            self.setLayout(hbox)
            self.setGeometry(300, 300, 300, 300)
            self.show()

            self.last = False
            self.timer = QTimer()
            self.timer.timeout.connect(self.switch)
            self.timer.start(500)

        def switch(self):
            """Switcher"""
            self.last = not self.last
            self.led.setState(self.last)

        @staticmethod
        def receive():
            """Receive stateChanged signal"""
            print('receive')

        @staticmethod
        def receive_with_args(state):
            """Receive stateChanged signal"""
            print('receive', state)


    main_w = Example()
    main_w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
