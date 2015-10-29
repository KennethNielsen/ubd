#!/usr/bin/env python
# pylint: disable=interface-not-implemented,invalid-name

"""A plugin for Qt Designer for the boolean input LightButton"""

import os
from PyQt4 import QtGui
from PyQt4.QtDesigner import QPyDesignerCustomWidgetPlugin
from ubd.pyqt.boolean_input import LightButton
from booleaninput_lightbutton_plugin_taskmenu import LightButtonTaskMenuFactory


class LightButtonPlugin(QPyDesignerCustomWidgetPlugin):
    """The LightButtonPlugin class

    Provides a Python custom plugin for Qt Designer by implementing the
    QDesignerCustomWidgetPlugin using a PyQt-specific custom plugin class.
    """

    def __init__(self, parent=None):
        super(LightButtonPlugin, self).__init__()
        self.initialized = False

    def initialize(self, formEditor):
        """Initialize the plugin"""
        if self.initialized:
            return

        # We register an extension factory to add a extension to each form's
        # task menu.
        manager = formEditor.extensionManager()
        if manager:
            self.factory = LightButtonTaskMenuFactory(manager)
            manager.registerExtensions(
                self.factory, "com.trolltech.Qt.Designer.TaskMenu"
            )

        self.initialized = True

    def isInitialized(self):
        """Return the initialized status"""
        return self.initialized

    def createWidget(self, parent):
        """Create a new instance of this widget"""
        return LightButton(parent)

    def name(self):
        """Return the name of the custom widget class"""
        return "LightButton"

    def group(self):
        """Return the Qt Designer Widget Group for this widget"""
        return "UBD widgets"

    def icon(self):
        """Return the icon used to represent the custom widget"""
        module_abs_path = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(module_abs_path, 'icons', 'light_button.png')
        return QtGui.QIcon(icon_path)

    def toolTip(self):
        """Return a tool tip"""
        return 'A toggle button that lights up when pressed (True)'

    def whatsThis(self):
        """Return a short description for the widget used as a help text"""
        what_is_this = 'This widget is used as a boolean input. It is a toggle button '\
                       'that lights up when pressed (in True state) which makes it '\
                       'easier to determine whether it is True of False at a glance'
        return what_is_this

    def isContainer(self):
        """Return whether the widget is a container"""
        return False

    def domXml(self):
        """Return an XML description for the widget"""
        return '<widget class="LightButton" name="lightbutton" />\n'

    def includeFile(self):
        """Return the modules that contains this class"""
        return "ubd.pyqt.boolean_input"
