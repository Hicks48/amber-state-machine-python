from __future__ import absolute_import
import unittest

from amber_automate.automate_builder import AutomateBuilder
from amber_automate.execution_builder import ExecutionBuilder

from amber_automate.execution_configuration import ExecutionConfiguration


class TestEndStates(unittest.TestCase):

    def test_end_state_stops_update(self):
        automate_builder = AutomateBuilder.create_automate_builder()
        automate_builder.add_state('start')
        automate_builder.add_state('error')
        automate_builder.add_state('A')
        automate_builder.add_state('end')

        automate_builder.add_transition('start', lambda i: i is not None, 'A')
        automate_builder.add_transition('A', lambda i: i is not None, 'end')

        automate_builder.set_start_state('start')
        automate_builder.set_error_state('error')

        automate_builder.add_end_state('end')

        amber_automate = automate_builder.build()

        exe_builder = ExecutionBuilder.create_exe_buidler()
        exe_builder.set_automate(amber_automate)

        exe_conf = ExecutionConfiguration()
        exe_conf.allow_to_stay_in_state_on_update = False
        exe_conf.allow_to_transit_to_multiple_states = True
        exe_conf.exit_when_end_state_is_encountered = True
        exe_builder.set_configuration(exe_conf)

        exe = exe_builder.build()

        exe.start()
        exe.update('1', '2')

        self.assertTrue(exe.is_at_end(), "Wasn't at end after end state was reached")