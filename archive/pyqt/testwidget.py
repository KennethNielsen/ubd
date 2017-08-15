"""Test widget"""

from PyQt4.QtGui import QWidget, QHBoxLayout, QLabel, QPushButton


class TestWidget(QWidget):
    """Labelled test widget"""

    def __init__(self, parent):
        print 'init'
        super(TestWidget, self).__init__(parent)
        self._box = QHBoxLayout()
        self.setLayout(self._box)
        self.label = QLabel('Test label', self)
        self.button = QPushButton('Test button', self)
        self._box.addWidget(self.label)
        self._box.addWidget(self.button)

    def moveEvent(self, *args, **kwargs):
        print 'move', args, kwargs
        super(TestWidget, self).moveEvent(*args, **kwargs)

    def resizeEvent(self, *args, **kwargs):
        print 'resize', args, kwargs
        super(TestWidget, self).resizeEvent(*args, **kwargs)

    def mouseDoubleClickEvent(self, *args, **kwargs):
        print 'mouse double click', args, kwargs
        super(TestWidget, self).mouseDoubleClickEvent(*args, **kwargs)
        
    def mouseMoveEvent(self, *args, **kwargs):
        print 'mouse move', args, kwargs
        super(TestWidget, self).mouseMoveEvent(*args, **kwargs)

    def mousePressEvent(self, *args, **kwargs):
        print 'mouse press', args, kwargs
        super(TestWidget, self).mousePressEvent(*args, **kwargs)

    def mouseReleaseEvent(self, *args, **kwargs):
        print 'mouse release', args, kwargs
        super(TestWidget, self).mouseReleaseEvent(*args, **kwargs)

