class Value(object):
    def __init__(self, v):
        self.v = v
        self.alias_ = None

    def alias(self, alias_):
        self.alias_ = alias_
        return self
