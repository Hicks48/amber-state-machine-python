#!/usr/bin/env python
# -*- coding: utf-8 -*-


class EpsilonInput(object):

    @staticmethod
    def get_epsilon_input():
        return EpsilonInput()

    def __init__(self):
        self.id = 'epsilon'

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if not other:
            return False

        return isinstance(other, EpsilonInput)

    def __ne__(self, other):
        return not self.__eq__(other)