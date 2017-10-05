
"""Implements a label widget"""

from PyQt5.QtWidgets import QLabel


class Label:
    """A common implementation of a widget with a label"""

    def __init__(self, parent, label, position):
        """Initialize labeled widget

        Args:
            parent (QWidget): The QWidget the label should be draw into
            label (str): The label text
            position (tuple): A tuple of x, y coordinates
        """
        self._label = QLabel(label, parent)
        self._label.move(*position)
