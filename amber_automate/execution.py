#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Execution(object):

    def __init__(self, automate, configuration):
        self.automate = automate

        self.current_states = set()
        self.encountered_end_states = set()

        self.configuration = configuration

        self.reset()

    def reset(self):
        self.current_states = set()

    def start(self):
        # Add current states and find epsilon transitions
        self.current_states.add(self.automate.start_state)
        with_epsilon_transition = self.automate.transition_table.get_next_states(next(iter(self.current_states)), None)
        self.current_states.update(with_epsilon_transition)

        # Look if end states are found and call on entry callback for each
        end_state_names = self.automate.get_end_state_names()
        end_states = set()
        for current_state in self.current_states:

            if current_state.on_entry:
                current_state.on_entry()

            if current_state.name in end_state_names:
                end_states.update(current_state)

        # Add end states if found
        if len(end_states) != 0:
            self.encountered_end_states.update(end_states)

        return not self.is_at_end()

    def update(self, *amber_inputs):

        if all(isinstance(n, list) for n in amber_inputs) and len(amber_inputs) == 1:
            return self._update_list(amber_inputs[0])
        else:
            return self._update_list(list(amber_inputs))

    def _update_list(self, inputs):
        input_accepted = list()

        for amber_input in inputs:
            input_accepted.append(self._update_single(amber_input))

        return input_accepted

    def _update_single(self, amber_input):

        # Check that has been started
        if len(self.current_states) == 0:
            raise Exception("Current states is empty. This is most likely because start method wasn't called before first update.")

        next_current_states = set()
        end_states = set()

        for current_state in self.current_states:

            # Get states to transit
            states_to_transit = self.automate.transition_table.get_next_states(current_state, amber_input)

            # Call on entry callback for each states which is to become current state
            # Do checks to find end states
            for transit_state in states_to_transit:

                if transit_state.on_entry:
                    transit_state.on_entry()

                if transit_state.name in self.automate.get_end_state_names():
                    end_states.update(transit_state)

            # If no states where to transit are found stay in current state
            # or go to error state depending on configuration
            if len(states_to_transit) == 0:

                if self.configuration.allow_to_stay_in_state_on_update:
                    # Call on stay callback
                    if current_state.on_stay:
                        current_state.on_stay()

                    # Add to next current state
                    next_current_states.add(current_state)
                    continue

                else:
                    # Call on exit callback
                    if current_state.on_exit:
                        current_state.on_exit()

                    error_state = self.automate.error_state
                    if error_state.on_entry:
                        error_state.on_entry()

                    next_current_states.add(error_state)

            # If has one transition then can transit
            elif len(states_to_transit) == 1:
                # Call on exit callback
                if current_state.on_exit:
                    current_state.on_exit()

                next_current_states.add(next(iter(states_to_transit)))

            else:
                #  Call on exit callback
                if current_state.on_exit:
                    current_state.on_exit()

                if self.configuration.allow_to_transit_to_multiple_states:
                    next_current_states.update(states_to_transit)
                else:
                    error_state = self.automate.error_state

                    if error_state.on_entry:
                        error_state.on_entry()

                    next_current_states.update(error_state)

        # Update current states
        self.current_states = set()
        self.current_states.update(next_current_states)

        # Update encountered end states
        if len(end_states) != 0:
            self.encountered_end_states.update(end_states)

        return not self.is_at_end()

    def is_at_end(self):

        # If only error state is left execution is done
        if len(self.current_states) == 1 and self.automate.error_state in self.current_states:
            return True

        # Otherwise is determined if end state was found
        if self.configuration.exit_when_end_state_is_encountered:
            return not len(self.encountered_end_states) == 0

        else:
            # If end states are treated as normal states then return false if all states are not in error state
            return False