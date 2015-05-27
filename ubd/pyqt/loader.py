"""Custom loader to hook up UBD functionality"""

from __future__ import print_function

import importlib
import pkgutil
import inspect

from PyQt4 import uic

from .. import pyqt as pyt


# Base print string used to print out the status of the loaded
BASESTRING = '{klass: <16}{ui: <20}{input: <20}{output}'


# Load all the UBD widget classes we know of into two lists
INPUTCLASSES = []
OUTPUTCLASSES = []
for importer, modname, ispkg in pkgutil.iter_modules(pyt.__path__):
    module = importlib.import_module('.' + modname, 'ubd.pyqt')
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            try:
                # The __ubd__ property identifies a widget as being either input or output
                direction = obj.__ubd__['direction']
            except AttributeError:
                pass
            else:
                if direction == 'input':
                    INPUTCLASSES.append(obj)
                elif direction == 'output':
                    OUTPUTCLASSES.append(obj)

# pylint: disable=too-few-public-methods


class InputOutput(object):
    """Create properties for a class of UBD widgets"""

    def __init__(self, main_ui, classes, specification):
        """Initialize the input output class

        Args:
            main_ui (QWidget): The widget that contains all the widgets
            classes (sequence): A sequence of classes to look for in main_ui to determine
                whether to add a property or not
            specification (str): A string describing what this IO class contains
        """
        super(InputOutput, self).__init__()
        self._specification = specification
        self.added_properties = set()
        for item in main_ui.__dict__.values():
            if item.__class__ in classes:
                property_functions = {}
                for getset in ['getter_function', 'setter_function']:
                    method_name = item.__ubd__[getset]
                    if method_name:
                        direction_func = getattr(item, method_name)
                    else:
                        direction_func = None
                    property_functions[getset] = direction_func
                setattr(self, str(item.objectName()), property(**property_functions))
                self.added_properties.add(item)


class Input(InputOutput):
    """Create properties for all UBD input widgets"""

    def __init__(self, main_ui):
        super(Input, self).__init__(main_ui, INPUTCLASSES, 'Input widgets')


class Output(InputOutput):
    """Create properties for all UBD output widgets"""

    def __init__(self, main_ui):
        super(Output, self).__init__(main_ui, OUTPUTCLASSES, 'Output widgets')


# pylint: disable=invalid-name
def loadUi(uifile, baseinstance=None, package='', resource_suffix='_rc'):
    """Load the uifile and create managed instances

    For help on the arguments, see the PyQt documentation.
    """
    loaded = uic.loadUi(uifile, baseinstance=baseinstance, package=package,
                        resource_suffix=resource_suffix)
    baseinstance.i = Input(baseinstance)
    baseinstance.o = Output(baseinstance)
    print_ui(loaded, baseinstance.i.added_properties, baseinstance.o.added_properties)
    return loaded


def print_ui(instance, inputs, outputs):
    """Print a overview of the available widgets and their codenames"""
    welcome = """
    The main GUI class for your program is: {}

    The GUI from your Qt Designer file have now been formed and loaded into
    the main GUI class.

    The widgets themselves have been bound to properties directly in the main
    class. They can be accessed e.g. by: self.my_button

    The managed UBD widgets have been bound to properties that can be used
    like variables. These properties are grouped by input and output widgets
    under the .i and .o property. To e.g. get the value for a toggle button
    do: self.i.my_toggle_button

    The bindings are summarized in the table below:
    """
    print(welcome.format(instance.__class__.__name__))
    infos = {}
    print(BASESTRING.format(klass='Type', ui='Widget property',
                            input='Input widget',
                            output='Output widget'))
    print(BASESTRING.format(klass='', ui='',
                            input='value property',
                            output='value property'))
    print('-' * 78)
    for item in instance.__dict__.values():
        try:
            objname = item.objectName()
        except AttributeError:
            continue

        infos = {
            'klass': item.__class__.__name__,
            'ui': '.{}'.format(objname),
            'input': '',
            'output': '',
        }
        if item in inputs:
            infos['input'] = '.i.{}'.format(objname)
        if item in outputs:
            infos['output'] = '.o.{}'.format(objname)
        print(BASESTRING.format(**infos))
    print()
