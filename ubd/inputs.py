"""This module contains the classes that define inputs"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty

from utils import show, myprint


def standard_kwargs_from_xml(element):
    kwargs = {}
    for tag in ['name', 'label']:
        kwargs[tag] = element.find(tag).text
    pos = []
    for tag in ['x', 'y']:
        pos.append(int(element.find(tag).text))
    kwargs['pos'] = pos
    return kwargs


class IntInput(BoxLayout):
    """This class represents an integer input"""

    value = NumericProperty(0)

    def __init__(self, name, label, pos, default, width=150, height=60):
        super(IntInput, self).__init__(orientation='vertical',
                                       size_hint=(None, None),
                                       width = width)
        self.name = name
        self.pos = pos
        # Add the input field
        self.field = TextInput(multiline=False, size_hint=(1, None))
        self.field.height = self.field.minimum_height + self.field.border[0]
        # Add the label
        self.label = Label(text=label, size_hint=(None, None))
        myprint(self.label.text_size)
        self.label.bind(texture_size=self.label.setter('size'))
        self.add_widget(self.label)
        self.add_widget(self.field)

        show(self)
        #show(self.label, (0, 1, 0))
        

    @classmethod
    def from_xml(cls, element):
        kwargs = standard_kwargs_from_xml(element)
        kwargs['default'] = int(element.find('default').text)
        return cls(**kwargs)
