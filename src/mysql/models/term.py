from sqlalchemy import Column, Integer, String
from application import Base

class Term(Base):
    __tablename__ = 'terms'

    term_id = Column(Integer, primary_key=True)
    name = Column(String(255))

    def __repr__(self):
        return "Term(name=%s)" % (self.name)

    def __init__(self, name):
        self.name = name