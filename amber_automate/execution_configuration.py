#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ExecutionConfiguration(object):

    @staticmethod
    def get_default_configuration():
        return ExecutionConfiguration()

    def __init__(self):
        self.allow_to_transit_to_multiple_states = True
        self.allow_to_stay_in_state_on_update = False
        self.exit_when_end_state_is_encountered = False