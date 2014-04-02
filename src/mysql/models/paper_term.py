from sqlalchemy import Column, Integer
from application import Base

class PaperTerm(Base):
    __tablename__ = 'papers-terms'

    paper_term_id = Column(Integer, primary_key=True)
    paper_id = Column(Integer)
    term_id = Column(Integer)

    def __init__(self, paper_id, term_id):
        self.paper_id = paper_id
        self.term_id = term_id
