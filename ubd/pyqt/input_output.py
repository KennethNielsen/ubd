"""Defines the input output objects"""


class InputOutputBase:
    """Input output base that defines getting items from widgets dicts"""
    def __init__(self):
        """Initialize object"""
        # We need to use the super.__setattr__ because we override __setattr__
        super().__setattr__('widgets', {})
        # Add seperate input and output objects, if instance is of the
        # combined InputOutput type
        if isinstance(self, InputOutput):
            super().__setattr__('inputs', Input())
            super().__setattr__('outputs', Output())

    def add_widget(self, widget):
        """Add a widget"""
        self.widgets[widget.name] = widget

    def __setattr__(self, name, value):
        """Set a widgets value by widget name"""
        self.widgets[name].value = value
        
    def __getattr__(self, name):
        """Get a widgets value by widget name"""
        try:
            return self.widgets[name].value
        except KeyError:
            raise AttributeError


class Input(InputOutputBase):
    """Collection of inputs"""
    pass


class Output(InputOutputBase):
    """Collection of outputs"""
    pass


class InputOutput(InputOutputBase):
    """Collection of inputs and outputs"""

    def __init__(self, all_widgets):
        super().__init__()
        for widget in all_widgets.values():
            if hasattr(widget, 'input_or_output'):
                self.add_widget(widget)

    def add_widget(self, widget):
        """Add a widget to input output objects"""
        self.widgets[widget.name] = widget
        if widget.input_or_output == 'input':
            self.inputs.add_widget(widget)
        elif widget.input_or_output == 'output':
            self.outputs.add_widget(widget)


        
