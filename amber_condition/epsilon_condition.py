#!/usr/bin/env python
# -*- coding: utf-8 -*-


class EpsilonConditionFactory(object):

    @staticmethod
    def create_epsilon_input():
        return EpsilonConditionFactory._epsilon_input

    @staticmethod
    def _epsilon_input(amber_input):
        return True