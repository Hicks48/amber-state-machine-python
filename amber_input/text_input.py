#!/usr/bin/env python
# -*- coding: utf-8 -*-

class TextInput(object):

    def __init__(self, text):
        self.text = text

    def __hash__(self):
        return hash(self.text)

    def __eq__(self, other):
        if not other:
            return False

        if isinstance(other, TextInput):
            return self.text == other.text
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)