
Widgets
=======

This page describes the design of the udb widgets. It serves as a
working document to document decisions and as a starting point when
creating a new widget.

Generel requirements
--------------------

.. todo:: Flesh this out to properly describe input and output widgets

The ubd widgets in general should have the following features:


 * **Labeled.** They should be labelled. Each ubd widget will have the notion of
   its own label, whose object exists only on the widget object.

Additionally for **input** widgets apply:

 * **value_changed signal.** It should have just a single signal
   ``value_changed``. It will emit the name of the widget and the
   value.
 * **No change of value until explicit submit.** The widget should not
   change value (not emit the ``value_changed`` signal) while typing a
   new value. Only upon hitting ``enter`` or (if configured as such)
   loosing focus (also by "tabbing out"), should the entered value be
   submitted for validation.
 * **get, set property.**. The value of the widget should be available
   for change via ``set_value`` and ``get_value`` methods **and** via
   a ``value`` property. The ``set_value`` should take a optional
   argument to disable emitting ``value_changed``.


API
---

The following should server as a template for implementing a new input
widget::

  from .common import LabeledWidget
  
  class MyNewWidget(LabeledWidget):
      """My new ... widget"""
  
      input_or_output = 'input'
  
      # The value changed
      value_changed = pyqtSignal([str, ...type_of_widget..])  # Update type
  
      def __init__(self, parent, name, position, default_value=0, **kwargs):
          """Initialize integer input
  
          Args:
              parent (QWidget): The QWidget this widget will be drawn into
              name (str): The name of this widget
              position (tuple): A tuple of x, y coordinates
              default_value (...): The default value of the input
              kwargs (dict): See LabeledWidget.__init__ for details
  
          """
          super().__init__(parent, name, kwargs)
  
	  # Create Qt widgets to use
	  # ...

          # Implement the rest of init

      def get_value(self):
          pass  # ...

      def set_value(self, value, do_not_emit_value_changed=False):
          pass  # ...

      value = property(get_value, set_value)
