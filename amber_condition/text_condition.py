#!/usr/bin/env python
# -*- coding: utf-8 -*-


class TextConditionFactory():

    @staticmethod
    def create_text_condition(text):
        return lambda amber_input: amber_input == text