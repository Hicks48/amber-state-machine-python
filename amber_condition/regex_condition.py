import re


class RegexConditionFactory(object):

    @staticmethod
    def create_regex_condition(regex):
        return lambda amber_input: re.match(regex, amber_input) != None