
"""An integer input implementation"""

from functools import partial
from PyQt5.QtCore import pyqtSignal, pyqtProperty
from PyQt5.QtWidgets import QSpinBox
from .common import LabeledWidget


class IntegerInput(LabeledWidget):
    """An integer input widget"""

    input_or_output = 'input'

    # The value changed
    value_changed = pyqtSignal([str, int])

    def __init__(self, parent, name, position, default_value=0, **kwargs):
        """Initialize integer input

        Args:
            parent (QWidget): The QWidget this integer input will be drawn into
            name (str): The name of this widget
            position (tuple): A tuple of x, y coordinates
            default_value (int): The default value of the input
            kwargs (dict): See LabeledWidget.__init__ for details

        """
        super().__init__(parent, name, kwargs)

        # Create spinbox
        self._spin_box = QSpinBox(parent, value=default_value)
        self._spin_box.move(*position)

        # Connect signal
        self._spin_box.valueChanged[int].connect(
            partial(self.value_changed.emit, self.name)
        )

    # FIXME Think about get set functionality and set without value_changed signal
    @property
    def value(self):
        return self._spin_box.value()

    @value.setter
    def value(self, value):
        self._spin_box.setValue(value)
