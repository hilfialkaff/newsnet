class Author:
    def __init__(self, name):
        self._name = name
        self._papers = {}

    def __repr__(self):
       return "Author(name='%s')" % (self._name)

    def add_paper(self, paper_id):
        self._papers[paper_id] = 1
