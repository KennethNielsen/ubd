"""Test widget"""

from PyQt4.QtGui import QWidget, QHBoxLayout

class TestWidget(QWidget):
    """Labellede test widget"""

    def __init__(self):
        super(TestWidget, self).__init__()
        self._box = QHBoxLayout()
        self.setLayout(self._box)
        self.label = QLabel('Test label')       
