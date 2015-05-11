#!/usr/bin/env python
# pylint: disable=C0103

"""Boolean input widgets"""

from __future__ import print_function

from PyQt4.QtCore import pyqtSignal, pyqtSlot  #, Qt
from PyQt4.QtGui import QPushButton

from common import COLOR_SCHEMES


class LightButton(QPushButton):
    """A toggle button that lights up when true (pressed in) state"""

    # The style sheet for the button, the color ints are formatted in, in __init__
    style_sheet = """
    QPushButton {{
        border: 1px solid black;
        border-radius: 4px;
        background-color: rgba({0}, {1}, {2}, {3});
        /*min-width: 80px;*/
        color: white;
        padding: 2px;
    }}

    QPushButton:pressed {{
        background-color: rgba({4}, {5}, {6}, {7});
        color: black;
        padding: 2px;
    }}

    QPushButton:checked {{
        background-color: rgba({4}, {5}, {6}, {7});
        color: black;
        padding: 2px;
    }}
        
    QPushButton:default {{
        border-color: navy;
    }}
    """

    # Define stateChanged signal, which can be emitted with a boolean or no arguments
    stateChanged = pyqtSignal([bool], [])

    def __init__(self, parent=None, text='button', color_scheme='green', default_state=False):
        super(LightButton, self).__init__(text=text, parent=parent)
        self.setCheckable(True)
        self._state = default_state
        self.setDown(default_state)

        # Get the RGBA ints for the colors
        true_rgba = COLOR_SCHEMES[color_scheme][True].getRgb()
        false_rgba = COLOR_SCHEMES[color_scheme][False].getRgb()

        self.setStyleSheet(self.style_sheet.format(*(false_rgba + true_rgba)))

    def state(self):
        """Return the boolean state"""
        return self.isChecked()

    @pyqtSlot(bool)
    @pyqtSlot(bool, bool)
    def setState(self, state, no_emit=False):
        """Set the boolean state"""
        self.setDown(state)
        if not no_emit:
            self.stateChanged.emit(self._state)

    def paintEvent(self, event):
        """Hacked paint event"""
        super(LightButton, self).paintEvent(event)



def main():
    """Elementary widget test"""
    import sys
    from PyQt4.QtGui import QApplication, QHBoxLayout, QWidget
    app = QApplication(sys.argv)

    class Example(QWidget):
        """Tester"""

        def __init__(self):
            super(Example, self).__init__()
            self.lightbutton = LightButton(text='Test', color_scheme='red')
            self.lightbutton.toggled.connect(self.toggle)
            hbox = QHBoxLayout()
            hbox.addWidget(self.lightbutton)
            self.setLayout(hbox)
            self.setGeometry(300, 300, 300, 300)
            self.show()

        @staticmethod
        def toggle(value):
            """Toggle callback"""
            print('toggle', value)

    main_w = Example()
    main_w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
