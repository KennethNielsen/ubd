
"""Implements loading definition files functionality"""

from yaml import load
from .integer_input import IntegerInput


ALL_WIDGETS = {
    'IntegerInput': IntegerInput,
}


def load_definition(definition_filepath):
    """Load and prepare GUI definition"""
    with open(definition_filepath) as file_:
        definition = load(file_)

    for widget_def in definition['main_window']['content']:
        _add_class(widget_def)
    return definition

def _add_class(widget_def):
    """Add the widget class to the definition"""
    widget_def['class'] = ALL_WIDGETS[widget_def['class']]

    # FIXME Add something here for widgets that can contain widgets,
    # iterate over content and call _add_class
