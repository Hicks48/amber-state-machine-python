#!/usr/bin/env python
# -*- coding: utf-8 -*-


class State(object):

    @staticmethod
    def create_state(name, on_entry=None, on_exit=None, on_stay=None):
        return State(name, on_entry, on_exit, on_stay)

    def __init__(self, name, on_entry, on_exit, on_stay):
        self.name = name
        self.on_entry = on_entry
        self.on_exit = on_exit
        self.on_stay = on_stay

    def __str__(self):
        return 'state:' + self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not other:
            return False

        if isinstance(other, State):
            return self.name == other.name
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
