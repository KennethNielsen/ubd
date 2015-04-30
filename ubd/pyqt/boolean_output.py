#!/usr/bin/env python

"""Boolean output widgets"""

#from PyQt4.QtCore import Qt, pyqtProperty, pyqtSignature, SIGNAL
#from PyQt4.QtGui import QDoubleSpinBox, QGridLayout, QLabel, QWidget
from PyQt4.QtGui import QWidget


class LED(QWidget):

    """A LED boolean output"""

    __pyqtSignals__ = ("latitudeChanged(double)", "longitudeChanged(double)")

    def __init__(self, parent=None):

        QWidget.__init__(self, parent)

        self.resize(100, 100)
        self.setStyleSheet('background-color: green;')


def main():
    """Elementary widget test"""
    import sys
    from PyQt4.QtGui import QApplication
    app = QApplication(sys.argv)
    widget = LED()
    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
