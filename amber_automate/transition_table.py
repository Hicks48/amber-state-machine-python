#!/usr/bin/env python
# -*- coding: utf-8 -*-

from amber_input.epsilon_input import EpsilonInput


class TransitionTable(object):

    def __init__(self, transition_table):
        self.transition_table = transition_table

    def add_state(self, state):
        entry = (state, None)
        self.transition_table[entry] = set()

    def get_all_transitions(self):
        return self.transition_table

    def get_all_transitions_for_state(self, source_state):
        transitions_for_state = {}

        for transition in self.transition_table:

            if transition[0] == source_state:
                transitions_for_state[transition] = self.transition_table[transition]

        return transitions_for_state

    def get_transitions_without_epsilon_transitions(self, state_input_pair):
        return self.transition_table[state_input_pair]

    def get_transition_with_epsilon(self, state_input_pair):
        target_states = None
        if state_input_pair in self.transition_table:
            target_states = self.transition_table[state_input_pair]

        if not target_states or len(target_states) == 0:
            return set()

        return self.get_epsilon_tranitions(target_states)

    def get_epsilon_tranitions(self, states):
        target_states = set()

        searched_states = set()
        states_to_search = set()

        states_to_search.update(states)

        while len(states_to_search) != 0:
            current_state = next(iter(states_to_search))

            target_states.add(current_state)

            # Update book keeping sets
            states_to_search.remove(current_state)
            searched_states.add(current_state)

            epsilon_target_states = None
            if  (current_state, EpsilonInput.get_epsilon_input()) in self.transition_table:
                epsilon_target_states = self.transition_table[(current_state, EpsilonInput.get_epsilon_input())]

            if not epsilon_target_states:
                continue

            for epsilon_target_state in epsilon_target_states:

                # Add if not already checked
                if epsilon_target_state not in searched_states:
                    states_to_search.add(epsilon_target_state)

        return target_states

    def add_transition(self, state_input_pair, transitions):

        if state_input_pair in self.transition_table:
            raise Exception("Given state input pair already exists in transition table")

        self.transition_table[state_input_pair] = transitions

    def update_transition(self, state_input_pair, transition_states):

        if not state_input_pair in self.transition_table:
            raise Exception("Given state input pair doesn't exists in transition table")

        self.transition_table[state_input_pair] = transition_states

    def delete_transitions_for_state_input_pair(self, state_input_pair):
        self.transition_table.pop_key(state_input_pair, None)

    def get_inputs(self):
        inputs = set()

        for state_input_pair in self.transition_table:
            inputs.update(state_input_pair[1])

        return inputs

    def get_source_states(self):
        states = set()

        for state_input_pair in self.transition_table:
            states.add(state_input_pair[0])

        return states

    def get_target_states(self):
        states = set()

        for state_set in self.transition_table.values():
            states.update(state_set)

        return states