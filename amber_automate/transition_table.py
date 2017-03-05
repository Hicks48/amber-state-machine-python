#!/usr/bin/env python
# -*- coding: utf-8 -*-


class TransitionTable(object):

    def __init__(self, transition_table):
        self.transition_table = transition_table

    def add_state(self, state):
        self.transition_table[state] = set()

    def add_transition(self, transition):

        if transition.source not in self.transition_table:
            raise Exception("Source state not in transition table")

        transitions = self.transition_table[transition.source]
        transitions.add(transition)
        self.transition_table[transition.source] = transitions

    def get_next_states(self, current_state, amber_input):
        next_states = set()

        transitions = self.transition_table[current_state]

        # Transitions with input
        for transition in transitions:
            if transition.is_open(amber_input):
                next_states.update(transition.targets)

        # Epsilon transitions
        for state in list(next_states):
            transitions = self.transition_table[state]
            for transition in transitions:
                if transition.is_open(None):
                    next_states.update(transition.targets)

        return next_states