import re


class RegexConditionFactory(object):

    @staticmethod
    def create_regex_condition(regex):
        return lambda amber_input: RegexConditionFactory._is_match(regex, amber_input)

    @staticmethod
    def _is_match(regex, amber_input):

        if amber_input is None:
            return False

        return re.match(regex, amber_input) is not None