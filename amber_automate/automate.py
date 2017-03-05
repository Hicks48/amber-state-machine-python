#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Automate(object):
    """
    This class presents automate structure. It contains the states and transitions between those states.
    Execution class is used to describe execution of automate.
    """

    def __init__(self, start_state, error_state, end_states, transition_table):
        """
        Create a new Automate object by providing start state, error state and transition table.
        Consider using AutomateBuilder class to initiate Automate object before using this.

        :param start_state: Start state is the state which is first current state in the execution process.
        :param error_state: Error state is a state in which execution proceeds when there is no defined transition with given input.
        :param end_states: End states are names of states which are to be treated as end states.
        :param transition_table: Transition table holds the information about the transitions between the states and the actual states them selves.
        """
        self.error_state = None
        self.start_state = None

        self.set_start_state(start_state)
        self.set_error_state(error_state)

        self.end_state_names = end_states
        self.transition_table = transition_table

    def get_end_state_names(self):
        return self.end_state_names

    def get_end_states(self):

        # Collect all states
        all_states = set()
        all_states.update(self.transition_table.get_source_states())
        all_states.update(self.transition_table.get_target_states())

        # Collect all end states
        end_states = set()
        for state in all_states:
            if state.name in self.end_state_names:
                end_states.update(state)

        return end_states

    def set_error_state(self, error_state):
        if not error_state:
            raise Exception("Can't set null error state")

        self.error_state = error_state

    def set_start_state(self, start_state):
        if not start_state:
            raise Exception("Can't set null start state.")

        self.start_state = start_state
