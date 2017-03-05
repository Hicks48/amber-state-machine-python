#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import unittest

from amber_automate.automate_builder import AutomateBuilder
from amber_automate.state import State
from amber_condition.text_condition import TextConditionFactory
from amber_condition.epsilon_condition import EpsilonConditionFactory
from amber_automate.execution import Execution
from amber_automate.execution_configuration import ExecutionConfiguration


class TestCallbacks(unittest.TestCase):

    def setUp(self):
        self.builder = AutomateBuilder.create_automate_builder()
        self.call_register = {}

    def test_should_call_callback_on_entry_at_start(self):
        automate = self._build_automate();
        exe = Execution(automate, ExecutionConfiguration.get_default_configuration())
        exe.start()

        self.assertTrue("start on entry" in self.call_register and self.call_register["start on entry"] == "entry", "Callback not called correctly")

    def test_should_call_callback_on_entry_at_entry(self):
        automate = self._build_automate()
        exe = Execution(automate, ExecutionConfiguration.get_default_configuration())
        exe.start()

        exe.update("1")
        self.assertTrue("a on entry" in self.call_register and self.call_register["a on entry"] == "entry", "Callback not called correctly")

    def test_should_call_on_entry_on_epsilon_transition(self):
        automate = self._build_automate()
        exe = Execution(automate, ExecutionConfiguration.get_default_configuration())
        exe.start()

        exe.update("1")
        exe.update("2")

        self.assertTrue("b on entry" in self.call_register and self.call_register["b on entry"] == "entry", "Callback not called correctly")
        self.assertTrue("c on entry" in self.call_register and self.call_register["c on entry"] == "entry", "Callback not called correctly")

    def test_should_call_on_enry_for_error_state(self):
        automate = self._build_automate()
        exe = Execution(automate, ExecutionConfiguration.get_default_configuration())
        exe.start()

        exe.update("invalid")
        self.assertTrue("error on entry" in self.call_register and self.call_register["error on entry"] == "entry", "Callback not called correctly")

    def test_should_call_on_exit_for_state(self):
        automate = self._build_automate()
        exe = Execution(automate, ExecutionConfiguration.get_default_configuration())
        exe.start()

        exe.update("1")
        self.assertTrue("start on exit" in self.call_register and self.call_register["start on exit"] == "exit", "Callback not called correctly")

    def test_should_call_on_exit_for_state_on_error(self):
        automate = self._build_automate()
        exe = Execution(automate, ExecutionConfiguration.get_default_configuration())
        exe.start()

        exe.update("invalid")
        self.assertTrue("start on exit" in self.call_register and self.call_register["start on exit"] == "exit", "Callback not called correctly")

    def test_should_call_on_stay_on_state(self):
        automate = self._build_automate()

        conf = ExecutionConfiguration()
        conf.allow_to_stay_in_state_on_update = True

        exe = Execution(automate, conf)
        exe.start()

        exe.update("1")
        exe.update("stay here")

        self.assertTrue("a on stay" in self.call_register and self.call_register["a on stay"] == "stay", "Callback not called correctly")
        self.assertTrue("a on exit" not in self.call_register, "Exit called when only stay was expected callback")

    def _build_automate(self):
        self.builder.add_state(State.create_state('start', self._create_callback('start on entry', 'entry'), self._create_callback('start on exit', 'exit')))
        self.builder.add_state(State.create_state("error", self._create_callback("error on entry", "entry"), self._create_callback("error on exit", "exit"), self._create_callback("error on stay", "stay")))
        self.builder.add_state(State.create_state("a", self._create_callback("a on entry", "entry"), self._create_callback("a on exit", "exit"), self._create_callback("a on stay", "stay")))
        self.builder.add_state(State.create_state("b", self._create_callback("b on entry", "entry"), self._create_callback("b on exit", "exit"), self._create_callback("b on stay", "stay")))
        self.builder.add_state(State.create_state("c", self._create_callback("c on entry", "entry"), self._create_callback("c on exit", "exit"), self._create_callback("c on stay", "stay")))

        self.builder.add_transition("start", TextConditionFactory.create_text_condition("1"), "a")
        self.builder.add_transition("a", TextConditionFactory.create_text_condition("2"), "b")
        self.builder.add_transition("b", EpsilonConditionFactory.create_epsilon_input(), "c")

        self.builder.set_start_state("start")
        self.builder.set_error_state("error")
        return self.builder.build()

    def _create_callback(self, name, msg):
        return lambda: self._input_to_call_register(name, msg)

    def _input_to_call_register(self, name, msg):
        self.call_register[name] = msg

if __name__ == '__main__':
    unittest.main()