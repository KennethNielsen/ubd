#!/usr/bin/env python
# pylint: disable=invalid-name

"""Task menu for Light button"""

import os
from PyQt4.QtCore import QVariant, SIGNAL
from PyQt4.QtDesigner import QExtensionFactory, QPyDesignerTaskMenuExtension,\
    QDesignerFormWindowInterface
from PyQt4.QtGui import QAction, QDialog, QApplication
from PyQt4.uic import loadUi
from ubd.pyqt.boolean_input import LightButton
from ubd.pyqt.common import COLOR_SCHEMES


class LightButtonMenuEntry(QPyDesignerTaskMenuExtension):
    """Task menu entry for a LightButton"""

    def __init__(self, widget, parent):
        super(LightButtonMenuEntry, self).__init__(parent)
        self.widget = widget

        # Create the action to be added to the form's existing task menu
        # and connect it to a slot in this class.
        self.editStateAction = QAction("UBD settings...", self)
        self.connect(self.editStateAction, SIGNAL("triggered()"), self.updateSettings)

    def preferredEditAction(self):
        """Return the preferred action"""
        return self.editStateAction

    def taskActions(self):
        """Return a list of task actions"""
        return [self.editStateAction]

    def updateSettings(self):
        """Update the settings"""
        dialog = LightButtonDialog(self.widget)
        dialog.exec_()


class LightButtonTaskMenuFactory(QExtensionFactory):
    """TaskMenuFactory for Lightbutton"""

    def __init__(self, parent=None):
        super(LightButtonTaskMenuFactory, self).__init__(parent)

    def createExtension(self, obj, iid, parent):  # pylint: disable=no-self-use
        """Return an object that represents a task meny entry"""
        if iid != "com.trolltech.Qt.Designer.TaskMenu":
            return None

        # Pass the instance of the custom widget to the object representing the task menu
        # entry
        if isinstance(obj, LightButton):
            return LightButtonMenuEntry(obj, parent)

        return None


class LightButtonDialog(QDialog):
    """The settings dialog for the LightButton"""

    def __init__(self, widget, parent=None):
        super(LightButtonDialog, self).__init__(parent)
        ui_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'ui', 'lightbutton_dialog.ui'
        )
        loadUi(ui_path, self)

        # Keep a reference to the widget in the form
        self.widget = widget

        # Init preview with same settings and add to layout
        self.previewWidget = LightButton()
        self.previewWidget.setEnabled(False)
        self.layout.addWidget(self.previewWidget, 0, 1)

        # Set preview and dialog values
        #- object
        self.previewWidget.setObjectName(widget.objectName())
        self.name.setText(self.widget.objectName())
        #- callback FIXME
        #- button text
        self.previewWidget.setText(widget.text())
        self.button_text.setText(widget.text())
        #- color scheme
        self.previewWidget.setColorscheme(widget.colorscheme())
        for key in COLOR_SCHEMES.keys():
            self.color_scheme.addItem(key)
        current_index = self.color_scheme.findText(widget.colorscheme())
        self.color_scheme.setCurrentIndex(current_index)
        #- initial state
        self.previewWidget.setDown(widget.isChecked())
        self.initial_state.setChecked(widget.isChecked())

        # Connect signals
        self.button_text.textChanged.connect(self.previewWidget.setText)
        self.color_scheme.currentIndexChanged[str].connect(self.previewWidget.setColorscheme)
        self.initial_state.toggled.connect(self.previewWidget.setChecked)
        self.buttonBox.accepted.connect(self.updateWidget)
        self.buttonBox.rejected.connect(self.reject)

    def updateWidget(self):
        """Update the widget"""
        formWindow = QDesignerFormWindowInterface.findFormWindow(self.widget)
        if formWindow:
            formWindow.cursor().setProperty(
                "objectName", QVariant(self.name.text()))
            # callback FIXME
            formWindow.cursor().setProperty(
                "text", QVariant(self.button_text.text()))
            formWindow.cursor().setProperty(
                "colorscheme_py", QVariant(self.color_scheme.currentText()))
            formWindow.cursor().setProperty(
                "text", QVariant(self.button_text.text()))
            formWindow.cursor().setProperty(
                "checked", QVariant(self.initial_state.isChecked()))
        self.accept()

if __name__ == '__main__':
    app = None
    if not app:
        app = QApplication([])

    window = LightButtonDialog(None)
    window.show()

    if app:
        app.exec_()
