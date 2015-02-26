"""Test of inplace assignments on properties

Status: Success. They work just fine
"""
from __future__ import print_function


class ValueHolder(object):
    def __init__(self, value=1):
        self.value = value


class Outer(object):
    def __init__(self):
        self._i = ValueHolder()

    @property
    def i(self):
        print('get')
        return self._i.value

    @i.setter
    def i(self, value):
        print('set')
        self._i.value = value


a = Outer()
print(a._i)
print(a.i)
print('==')
a.i += 8
print('==')
print(a._i.value)
print(a.i)
