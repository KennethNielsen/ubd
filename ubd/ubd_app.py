"""This module contains the UDBApp class, which is the main builder
class for UDB.
"""

# Standard lib
import xml.etree.ElementTree as etree
# Third party
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.event import EventDispatcher
# Own
from inputs import IntInput
from utils import show


class MainUBD(FloatLayout):

    def __init__(self, gui_def, *args, **kwargs):
        super(MainUBD, self).__init__(*args, **kwargs)

        # Get gui def root
        root = etree.parse(gui_def).getroot()

        # Set window and make widget occupy all of the window
        settings = root.find('settings')
        width = int(settings.find('width').text)
        height = int(settings.find('height').text)
        Window.size = (width, height)
        self.size_hint = None, None
        self.size = (width, height)

        # Inputs
        self.input = {}
        self.input_gui = {}
        for element in root.findall('input'):
            self._add_input(element)

        # Add a float layout
        #self.layout = FloatLayout(size=(width, height))
        #self.add_layout(self.layout)

    def _add_input(self, element):
        """Add an input"""
        input_class = INPUT_CLASSES[element.find('type').text]
        instance = input_class.from_xml(element)
        self.add_widget(instance)
        #self.input[instance.name] = instance.value


INPUT_CLASSES = {
    'int': IntInput
}
