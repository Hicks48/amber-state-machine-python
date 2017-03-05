#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import unittest

from amber_automate.automate_builder import AutomateBuilder
from amber_condition.text_condition import TextConditionFactory
from amber_automate.state import State
from amber_automate.execution import Execution
from amber_automate.execution_configuration import ExecutionConfiguration


class TestAutomate(unittest.TestCase):

    @staticmethod
    def print1():
        print("in state pair")

    @staticmethod
    def print2():
        print("in state non pair")

    def test_basics(self):
        # Build automate
        builder = AutomateBuilder.create_automate_builder()
        builder.add_state("error")
        builder.add_state(State.create_state("pair", TestAutomate.print1))
        builder.add_state(State.create_state("non pair", TestAutomate.print2))

        builder.set_error_state("error")
        builder.set_start_state("pair")

        builder.add_transition("pair", TextConditionFactory.create_text_condition("1"), "non pair")
        builder.add_transition("pair", TextConditionFactory.create_text_condition("0"), "pair")
        builder.add_transition("non pair", TextConditionFactory.create_text_condition("1"), "pair")
        builder.add_transition("non pair", TextConditionFactory.create_text_condition("0"), "non pair")

        amber_aut = builder.build()
        amber_exe = Execution(amber_aut, ExecutionConfiguration.get_default_configuration())

        amber_exe.start()
        amber_exe.update("0", "1", "0", "0", "1")

        self.assertTrue(len(amber_exe.current_states) == 1)
        self.assertTrue(next(iter(amber_exe.current_states)).name == 'pair')

if __name__ == '__main__':
    unittest.main()