
"""Float input widget"""

# Started from: https://gist.github.com/jdreaver/0be2e44981159d0854f5

# TODO: Look more into the RE
# TODO: Read more into code

from __future__ import print_function

import re

import numpy as np
from PyQt4.QtGui import QValidator, QDoubleSpinBox


# Regular expression to find floats. Match groups are the whole string, the
# whole coefficient, the decimal part of the coefficient, and the exponent
# part.
_float_re = re.compile(r'(([+-]?\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)')

def valid_float_string(string):
    match = _float_re.search(string)
    return match.groups()[0] == string if match else False


class FloatValidator(QValidator):

    def validate(self, string, position):
        string = str(string)
        if valid_float_string(string):
            return self.Acceptable, position
        if string == "" or string[position-1] in 'Ee.-+':
            return self.State(self.Intermediate), position
        return self.State(self.Invalid), position

    def fixup(self, text):
        match = _float_re.search(text)
        return match.groups()[0] if match else ""


class ScientificDoubleSpinBox(QDoubleSpinBox):

    def __init__(self, *args, **kwargs):
        super(ScientificDoubleSpinBox, self).__init__(*args, **kwargs)
        self.setKeyboardTracking(False)
        self.setMinimum(-np.inf)
        self.setMaximum(np.inf)
        self.validator = FloatValidator()
        self.setDecimals(1000)

    def validate(self, text, position):
        return self.validator.validate(text, position)

    def fixup(self, text):
        return self.validator.fixup(text)

    def valueFromText(self, text):
        return float(text)

    def textFromValue(self, value):
        return format_float(value)

    def stepBy(self, steps):
        text = self.cleanText()
        groups = _float_re.search(text).groups()
        decimal = float(groups[1])
        decimal += steps
        new_string = "{:g}".format(decimal) + (groups[3] if groups[3] else "")
        self.lineEdit().setText(new_string)
        self.setValue(self.valueFromText(new_string))


def format_float(value):
    """Modified form of the 'g' format specifier."""
    string = "{:g}".format(value).replace("e+", "e")
    string = re.sub("e(-?)0*(\d+)", r"e\1\2", string)
    return string


def dev():
    """Function to test the widget during development"""
    import sys
    import time
    from PyQt4.QtGui import QApplication, QHBoxLayout, QWidget
    app = QApplication(sys.argv)

    class Example(QWidget):
        """Tester"""

        def __init__(self):
            super(Example, self).__init__()
            self.scientific = ScientificDoubleSpinBox()
            self.scientific.valueChanged.connect(self.value_changed)
            hbox = QHBoxLayout()
            hbox.addWidget(self.scientific)
            self.setLayout(hbox)
            self.setGeometry(300, 300, 300, 300)
            self.show()

        @staticmethod
        def value_changed(value):
            """Toggle callback"""
            print('changed', value)

    main_w = Example()
    main_w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    dev()
