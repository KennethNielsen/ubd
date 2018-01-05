
from .common import LabeledWidget


class IntegerOutput(LabeledWidget):
    """An integer output"""

    input_or_output = 'output'

    def __init__(self, parent, name, position, default_value=0, **kwargs):
        """Initialize integer input

        Args:
            parent (QWidget): The QWidget this integer input will be drawn into
            name (str): The name of this widget
            position (tuple): A tuple of x, y coordinates
            default_value (int): The default value of the input
            kwargs (dict): See LabeledWidget.__init__ for details

        """
        pass
