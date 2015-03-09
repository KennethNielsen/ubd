# pylint: disable=too-few-public-methods,no-self-use

"""Multiple mixin test

This tech test has the prupose of trying to figure out whether the
different roles of widgets, Container and Movable, could be defined
via mixin classes.

Outcome: Success

"""


from __future__ import print_function


class Label(object):
    """Label"""
    def __init__(self):
        print("Label __init__")


class Tab(object):
    """Tab"""
    def __init__(self):
        print("Tab __init__")


class Widget(object):
    """Widget"""
    def __init__(self):
        print("Widget __init__")

    def add_widget(self, widget):
        """Adds a widget"""
        print("Widget add_widget", widget)


class MovableMixin(object):
    """MovableMixin"""
    def __init__(self):
        print("MovableMixin __init__")
        self.parent = None
        super(MovableMixin, self).__init__()

    def set_parent(self, parent):
        """Sets the parent of the widget"""
        print(self.__class__, "set parent to", parent)
        self.parent = parent

    def detect_move(self):
        """Detect a move and report it to the parent"""
        self.parent.report_move_to_parent(self)

    def do_move(self):
        """Perform the ordered move"""
        print("MovableMixin", self, "has been told to move")


class ContainerMixin(object):
    """ContainerMixin"""
    def __init__(self):
        print("ContainerMixin __init__")
        self.content = []
        super(ContainerMixin, self).__init__()

    def append(self, widget):
        """Append a widget to a container"""
        print('ContainerMixin append', widget)
        self.content.append(widget)
        widget.set_parent(self)
        self.add_widget(widget)

    def report_move_to_parent(self, movable):
        """Report move to parent"""
        print("ContainerMixin", self, "has been told by", movable,
              "that it has moved")
        movable.do_move()


class MyBase(ContainerMixin, Widget):
    """MyBase"""
    def __init__(self):
        print("MyBase __init__")
        super(MyBase, self).__init__()


class MyTab(MovableMixin, ContainerMixin, Tab):
    """MyTab"""
    def __init__(self):
        print("MyTab __init__")
        self.parent = None
        super(MyTab, self).__init__()


class MyLabel(MovableMixin, Label):
    """MyLabel"""
    def __init__(self):
        print("MyLabel __init__")
        super(MyLabel, self).__init__()


if __name__ == '__main__':
    print("###")
    BASE = MyBase()
    print("###")
    TAB = MyTab()
    print("###")
    BASE.append(TAB)
    print("###")
    print(TAB.parent)
    print("###")
    TAB.detect_move()
