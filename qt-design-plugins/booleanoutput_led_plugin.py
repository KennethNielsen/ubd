#!/usr/bin/env python
# pylint: disable=interface-not-implemented,invalid-name

"""A plugin for Qt Designer for the boolean output LED"""

import os
from PyQt4 import QtGui
from PyQt4.QtDesigner import QPyDesignerCustomWidgetPlugin
from ubd.pyqt.boolean_output import LED
from booleanoutput_led_plugin_taskmenu import LEDTaskMenuFactory


class LEDPlugin(QPyDesignerCustomWidgetPlugin):
    """The LEDPlugin class

    Provides a Python custom plugin for Qt Designer by implementing the
    QDesignerCustomWidgetPlugin using a PyQt-specific custom plugin class.
    """

    def __init__(self, parent=None):
        super(LEDPlugin, self).__init__()
        self.initialized = False

    def initialize(self, formEditor):
        """Initialize the plugin"""
        if self.initialized:
            return

        # We register an extension factory to add a extension to each form's
        # task menu.
        manager = formEditor.extensionManager()
        if manager:
            self.factory = LEDTaskMenuFactory(manager)
            manager.registerExtensions(
                self.factory, "com.trolltech.Qt.Designer.TaskMenu"
            )

        self.initialized = True

    def isInitialized(self):
        """Return the initialized status"""
        return self.initialized

    def createWidget(self, parent):
        """Create a new instance of this widget"""
        return LED(parent)

    def name(self):
        """Return the name of the custom widget class"""
        return "LED"

    def group(self):
        """Return the Qt Designer Widget Group for this widget"""
        return "UBD widgets"

    def icon(self):
        """Return the icon used to represent the custom widget"""
        module_abs_path = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(module_abs_path, 'icons', 'LED.png')
        return QtGui.QIcon(icon_path)

    def toolTip(self):
        """Return a tool tip"""
        return 'An LED boolean indicator'

    def whatsThis(self):
        """Return a short description for the widget used as a help text"""
        what_is_this = 'This widget is used as a boolean output. It is a LED that lights '\
                       'up when set to True.'
        return what_is_this

    def isContainer(self):
        """Return whether the widget is a container"""
        return False

    def domXml(self):
        """Return an XML description for the widget"""
        return '<widget class="LED" name="LED" />\n'

    def includeFile(self):
        """Return the modules that contains this class"""
        return "ubd.pyqt.boolean_output"
