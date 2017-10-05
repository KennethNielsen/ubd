

"""My test program"""

import sys
from PyQt5.QtWidgets import QApplication
from ubd.pyqt.window import UBDWindow

# 20:42

class MyProgram(UBDWindow):
    """My super fancy program"""

    def __init__(self):
        super().__init__('definition.yaml')

    def change(self, name, value):
        print(self.i.integer_input1, self.i.integer_input2)
        


app = QApplication(sys.argv)
w = MyProgram()
w.show()
sys.exit(app.exec_())


#w.resize(500, 500)
#w.move(200, 200)
#w.setWindowTitle('Simple')
