"""The implementation of the main window"""

from yaml import load
from PyQt5.QtWidgets import QWidget
from .input_output import InputOutput
from .definition import load_definition


class UBDWindow(QWidget):

    def __init__(self, definition_filepath):
        super().__init__()
        # Load the definition and check the version
        self.definition = load_definition(definition_filepath)
        self._version_check()

        # Form all widgets and add them to the GUI
        self._add_widgets()

        # Collect all widgets in a dict
        self.widgets = {}
        self._collect_all_widgets(self.definition['main_window'])

        # Bind all automatic callbacks
        self._bind_callbacks()

        # Form input/output shortcut objects
        self.io = InputOutput(self.widgets)
        self.i = self.io.inputs
        self.o = self.io.outputs

    def _version_check(self):
        if self.definition['style'] != 'ubd':
            message = 'The layout file does not appear to be for UBD'
            raise RuntimeError(message)
        if self.definition['version'] != 0:
            message = 'This version of UBD only supports version 0 of layout files'
            raise RuntimeError(message)

    def _add_widgets(self):
        """Configures window and asks the widgets to add them selves"""
        main_window_def = self.definition['main_window']
        self.resize(*main_window_def['size'])
        # FIXME w.move(200, 200)
        self.setWindowTitle(main_window_def['title'])

        for widget_def in main_window_def['content']:
            klass = widget_def.pop('class')
            obj = klass(self, **widget_def)
            widget_def['object'] = obj
            #self.widgets[obj.name] = obj

    def _collect_all_widgets(self, definition_part):
        """Collect all the objects in the definition"""
        # If the def part has an object, add it
        if 'object' in definition_part:
            self.widgets[definition_part['name']] = definition_part['object']

        # If the def part has content, recursive process that
        if 'content' in definition_part:
            for inner_definition_part in definition_part['content']:
                self._collect_all_widgets(inner_definition_part)

    def _bind_callbacks(self):
        """Bind all callbacks to appropriate methods"""
        for widget in self.widgets.values():
            if widget.callback_name is not None:
                callback_function = getattr(self, widget.callback_name)
                widget.value_changed.connect(callback_function)
