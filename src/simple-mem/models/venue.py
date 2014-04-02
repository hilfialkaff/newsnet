class Venue():
    def __init__(self, name):
        self._name = name
        self._papers = {} # id of papers submitted to this conference

    def __repr__(self):
       return "Venue(name='%s')" % (self._name)

    def add_paper(self, paper_id):
        self._papers[paper_id] = 1
