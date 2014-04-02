class Paper():
    def __init__(self, name, year):
        self._name = name
        self._year = year
        self._terms = {}
        self._cited_by = {}
        self._cites = {}

    def __repr__(self):
       return "Paper(name='%s')" % (self.name)

    def add_term(self, term_id):
        self._terms[term_id] = 1

    def add_cited_by(self, paper_id):
        self._cited_by[paper_id] = 1

    def add_cites(self, paper_id):
        self._cites[paper_id] = 1
