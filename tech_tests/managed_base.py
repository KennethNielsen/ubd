"""Base for managed widget test"""

from __future__ import print_function


from PySide import QtGui


class Inputs(object):
    """Inputs"""

    def __init__(self, parent):
        self._line = QtGui.QLineEdit(parent)
        self._line.resize(self._line.sizeHint())
        self._line.setText('Default')
        self._line.textEdited.connect(parent.printer)

        self._spin = QtGui.QSpinBox(parent)
        self._spin.move(0, 30)
        self._spin.valueChanged.connect(parent.printer)

    @property
    def myint(self):
        return self._spin.value()

    @myint.setter
    def myint(self, value):
        self._spin.setValue(value)

    @property
    def myline(self):
        return self._line.text()

    @myline.setter
    def myline(self, value):
        self._line.setText(value)


class Outputs(object):
    """Outputs"""

    def __init__(self, parent):
        self._lineout = QtGui.QLineEdit(parent, 'Defaultout')
        self._lineout.setReadOnly(True)
        self._lineout.move(0, 60)

    @property
    def lineout(self):
        return self._lineout.text()

    @lineout.setter
    def lineout(self, value):
        self._lineout.setText(value)


class UbdApp(QtGui.QWidget):
    """The UBD App class"""

    def __init__(self):
        keys_in_app = set(self.__class__.__dict__.keys())
        #print(keys_in_app)
        keys_in_widget = set(dir(QtGui.QWidget))
        #print(keys_in_widget)
        print("Keys in common", keys_in_widget.intersection(keys_in_app))

        super(UbdApp, self).__init__()
        self.i = Inputs(self)
        self.o = Outputs(self)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Managed Test')
        self.show()

