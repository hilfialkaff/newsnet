class Term():
    def __init__(self, name):
        self._name = name

    def __repr__(self):
       return "Term(name='%s')" % (self._name)
