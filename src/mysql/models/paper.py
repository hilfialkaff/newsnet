from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import relationship
from application import Base

class Paper(Base):
    __tablename__ = 'papers'

    paper_id = Column(Integer, primary_key=True)
    name = Column(String(700))
    year = Column(Integer)

    def __repr__(self):
       return "Paper(name='%s')" % (self.name)

    def __init__(self, name, year):
        self.name = name
        self.year = year
