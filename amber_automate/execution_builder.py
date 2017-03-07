#!/usr/bin/env python
# -*- coding: utf-8 -*-

from amber_automate.execution import Execution
from amber_automate.execution_configuration import ExecutionConfiguration


class ExecutionBuilder(object):

    @staticmethod
    def create_exe_buidler():
        return ExecutionBuilder()

    def __init__(self):
        self.configuration = ExecutionConfiguration.get_default_configuration()
        self.automate = None

    def set_automate(self, automate):
        self.automate = automate
        return self

    def set_configuration(self, configuration):
        self.configuration = configuration
        return self

    def build(self):
        if not self.automate:
            raise Exception("Automate wasn't set for execution before trying to build it")

        return Execution(self.automate, self.configuration)

