
"""Common components"""

from collections import OrderedDict
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QObject
from .label import Label

# Used for boolean outputs
COLOR_SCHEMES = OrderedDict((
    ('green', {False: QColor('dark green'), True: QColor('lawn green')}),
    ('red', {False: QColor('dark red'), True: QColor('red')}),
    ('blue', {False: QColor('dark blue'), True: QColor('deep sky blue')}),
))


class LabeledWidget(QObject):
    """An abstract labeled widget"""

    def __init__(self, parent, name, kwargs):
        """Initialize object

        Args:
            parent (QWidget): The parent widget
            name (str): The name of the labeled widget
            kwargs (dict): A dictionary of additional arguments. See below.

        Possible keys in kwargs are:
         * callback: Holds the name of callback method in the main window
         * label: dict which holds label band position arguments for a Label

        """
        super().__init__(parent)
        # Set name and callback name
        self.name = name
        self.callback_name = kwargs.get('callback')

        # Add label if one is defined
        if 'label' in kwargs:
            self.label = Label(parent=parent, **kwargs['label'])
