#!/usr/bin/env python
# pylint: disable=C0103

"""Boolean input widgets"""

from __future__ import print_function

from PyQt4.QtCore import pyqtSignal, pyqtSlot, pyqtProperty
from PyQt4.QtGui import QPushButton

from .common import COLOR_SCHEMES


class LightButton(QPushButton):
    """A toggle button that lights up when true (pressed in) state

    This class defines the ``stateChanged`` signal which optionally provides the new state
    of the button. The difference between the ``stateChanged`` and the ``toggled`` signal
    is that when using the setState method, it is optional (and off by default) whether to
    also emit the stateChanged signal. Hence it is useful as a callback only when the
    button is actually pressed.

    """

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

    def __init__(self, parent=None, text='light_button', color_scheme='green',
                 initial_state=False):
        super(LightButton, self).__init__(text=text, parent=parent)
        self.setCheckable(True)
        self.setChecked(initial_state)
        self._color_scheme = None
        self.setColorscheme(color_scheme)
        self.toggled.connect(self.stateChanged)

    def state(self):
        """Return the boolean state"""
        return self.isChecked()

    @pyqtSlot(bool)
    @pyqtSlot(bool, bool)
    def setState(self, state, emit_state_changed=False):
        """Set the boolean state"""
        if not emit_state_changed:
            self.toggled.disconnect(self.stateChanged)
        self.setChecked(state)
        if not emit_state_changed:
            self.toggled.connect(self.stateChanged)

    def paintEvent(self, event):
        """Hacked paint event"""
        super(LightButton, self).paintEvent(event)

    def colorscheme(self):
        """Return the current colorscheme"""
        return self._color_scheme

    def setColorscheme(self, color_scheme):
        """Set the colorscheme"""
        self._color_scheme = str(color_scheme)
        # Get the RGBA ints for the colors
        true_rgba = COLOR_SCHEMES[self._color_scheme][True].getRgb()
        false_rgba = COLOR_SCHEMES[self._color_scheme][False].getRgb()
        self.setStyleSheet(self.style_sheet.format(*(false_rgba + true_rgba)))

    colorscheme_py = pyqtProperty(str, colorscheme, setColorscheme)


def main():
    """Elementary widget test"""
    import sys
    import time
    from PyQt4.QtGui import QApplication, QHBoxLayout, QWidget
    from threading import Thread
    app = QApplication(sys.argv)

    class Example(QWidget):
        """Tester"""

        def __init__(self):
            super(Example, self).__init__()
            self.lightbutton = LightButton(text='Button', color_scheme='green')
            self.lightbutton.toggled.connect(self.toggle)
            self.lightbutton.stateChanged.connect(self.changed)
            hbox = QHBoxLayout()
            hbox.addWidget(self.lightbutton)
            self.setLayout(hbox)
            self.setGeometry(300, 300, 300, 300)
            self.show()
            thread = Thread(target=self.use_state_change)
            thread.start()

        def use_state_change(self):
            """Use the state change method"""
            time.sleep(1)
            self.lightbutton.setState(True)

        @staticmethod
        def toggle(value):
            """Toggle callback"""
            print('toggle', value)

        @staticmethod
        def changed(value):
            """Toggle callback"""
            print('changed', value)

    main_w = Example()
    main_w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
