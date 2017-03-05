#!/usr/bin/env python
# -*- coding: utf-8 -*-

from amber_automate.automate import Automate
from amber_automate.state import State
from amber_automate.transition_table import TransitionTable


class AutomateBuilder(object):

    @staticmethod
    def create_automate_builder():
        return AutomateBuilder()

    def __init__(self):
        self.start_state = None
        self.error_state = None

        self.transition_table = {}
        self.states = {}
        self.end_state_names = set()

    def set_start_state(self, start):
        if isinstance(start, str):
            return self._set_start_state_with_name(start)
        elif isinstance(start, State):
            return self._set_start_state_with_state(start)
        else:
            raise Exception("In correct parameters given. Accepts str or State.")

    def _set_start_state_with_name(self, name):

        if name not in self.states:
            raise Exception("No state named " + name + " found. Use addState first.")

        self.start_state = self.states[name]

        return self

    def _set_start_state_with_state(self, start_state):

        if not start_state.name in self.states:
            raise Exception("No state named " + start_state.name + " found. Use addState first.")

        self.start_state = start_state

        return self

    def set_error_state(self, error):
        if isinstance(error, str):
            return self._set_error_state_with_name(error)
        elif isinstance(error, State):
            return self._set_error_state_with_state(error)
        else:
            raise Exception("In correct parameters given. Accepts str or State.")

    def _set_error_state_with_name(self, name):

        if not name in self.states:
            raise Exception("No state named " + name + " found. Use addState first.")

        self.error_state = self.states[name]

        return self

    def _set_error_state_with_state(self, error_state):

        if error_state.name not in self.states:
            raise Exception("No state named " + error_state.name + " found. Use addState first.");

        self.error_state = error_state

        return self

    def add_state(self, state):
        if isinstance(state, str):
            return self._add_state_with_name(state)
        elif isinstance(state, State):
            return self._add_state_with_state(state)
        else:
            raise Exception("In correct parameters given. Accepts str or State.")

    def _add_state_with_name(self, name):

        if name in self.states:
            raise Exception("Already has a state named " + name + ". Can't have two states with same name.")

        self.states[name] = State.create_state(name)

        return self

    def _add_state_with_state(self, state):

        if state.name in self.states:
            raise Exception("Already has a state named " + state.name + ". Can't have to states with same name.")

        self.states[state.name] = state

        return self

    def add_end_state(self, state):
        if isinstance(state, str):
            return self._add_end_state_with_name(state)
        elif isinstance(state, State):
            return self._add_end_state_with_state(state)
        else:
            raise Exception("In correct parameters given. Accepts str or State.")

    def _add_end_state_with_state(self, end_state):

        if end_state.name not in self.states:
            raise Exception("No state named " + end_state.name + " found. Use addState first.")

        self.end_state_names.update(end_state.name)

        return self

    def _add_end_state_with_name(self, name):

        if name not in self.states:
            raise Exception("No state named " + name + " found. Use addState first.")

        self.end_state_names.update(name)

        return self

    def add_transition(self, source_state, amber_input, *target_states):
        # Name is string and tuple contains only one list
        if isinstance(source_state, str) and all(isinstance(n, list) for n in target_states) and len(target_states) == 1:
            return self._add_transition_with_list(source_state, amber_input, target_states)

        # Name is string and target states contains strings
        elif isinstance(source_state, str) and all(isinstance(n, str) for n in target_states):
            return self._add_transition_with_list(source_state, amber_input, list(target_states))

        # Source state is State and target states contains states
        elif isinstance(source_state, State) and all(isinstance(n, State) for n in target_states):
            return self._add_transition_with_state(source_state, amber_input, target_states)

        # Raise exception if didn't get correct types as input
        else:
            raise Exception("Didn't get input with correct types. Accepts <str> <amber_input> <tuple of strings>, <str> <amber_input> <list of strings> or <state> <amber_input> <tuple of states>.")

    def _add_transition_with_list(self, source_state_name, amber_input, target_state_names):

        if source_state_name not in self.states:
            raise Exception("No state named " + source_state_name + " found. Use addState first.")

        state_input_pair = (self.states[source_state_name], amber_input)

        transition_states = set()
        for target_state_name in target_state_names:

            if target_state_name not in self.states:
                raise Exception("No state named " + source_state_name + " found. Use addState first.")

            transition_states.add(self.states[target_state_name])

        # Update transition table
        if state_input_pair not in self.transition_table:
            self.transition_table[state_input_pair] = transition_states

        else:
            original_target_states = self.transition_table[state_input_pair]
            original_target_states.update(transition_states)
            self.transition_table[state_input_pair] = original_target_states

        return self

    def _add_transition_with_state(self, source_state, amber_input, *target_states):

        # Check source state
        if source_state.name not in self.states:
            raise Exception("No state named " + source_state.name + " found. Use addState first.")

        # Create source state input pair
        state_input_pair = (self.states[source_state.name], amber_input)

        # Check transition states
        transition_states = set()
        for target_state in target_states:

            if not target_state.name in self.states:
                raise Exception("No state named " + target_state.name + " found. Use addState first.")

            transition_states.update(target_state)

        # Update transition table
        if state_input_pair not in self.transition_table:
            self.transitionTable[state_input_pair] = transition_states

        else:
            original_target_states = self.transition_table[state_input_pair]
            original_target_states.update(transition_states)
            self.transition_table[state_input_pair] = original_target_states

        return self

    def clear(self):
        self.transition_table = {}
        self.states = {}
        self.end_state_names = set()
        self.start_state = None
        self.error_state = None

    def build(self):

        if not self.start_state:
            raise Exception("Start state has not been set.")

        if not self.error_state:
            raise Exception("Error state has not been set.")

        return Automate(self.start_state, self.error_state, self.end_state_names, TransitionTable(self.transition_table))