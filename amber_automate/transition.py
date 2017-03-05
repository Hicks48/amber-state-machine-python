class Transition(object):

    def __init__(self, source, is_open_func, targets):
        self.source = source
        self.is_open_func = is_open_func
        self.targets = targets

    def is_open(self, amber_input):
        return self.is_open_func(amber_input)

    def __hash__(self):
        return hash(self.source)

    def __eq__(self, other):

        if not isinstance(other, Transition):
            return False

        return other.source == self.source and other.targets.issubset(self.targets) and self.targets.issubset(other.targets)

    def __ne__(self, other):
        return not self.__eq__(other)