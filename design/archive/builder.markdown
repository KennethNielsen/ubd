Text page for design considerations for the Builder.


Overall data structure
======================

Each composite widget (label and widget) is composed of two individual
widgets, which are only linked together through a data structure.

Move and resize
===============

To account for the idea of having widgets inside widgets e.g. buttons inside
tab widgets, there will be written support code in the form of a mixin class,
that makes the classic widgets support the roles on being inner and outer
widgets. In these roles the following will hapen:

* Outer widget implement selection by mouse rectangle by selecting the
  widgets that are inclosed
* Widget are selectable by a single left click
* The widgets monitor whether they have been resized or moved
 * On resize, a widget will report to the outer widget to reduce the
   selection to just itself and then resize themselves
 * On move, they report the move to the outer widget, which moves all
   the widgets in the current selection

The mixin should have `__init__` options to sugges whether they
support the inner and outer role.
