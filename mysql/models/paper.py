from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from application import Base

class Paper(Base):
    __tablename__ = 'papers'

    paper_id = Column(Integer, primary_key=True)
    name = Column(String(500))

    terms = relationship("Term", cascade="all, delete, delete-orphan")
    venue_id = Column(Integer, ForeignKey('venues.venue_id'))
    year = Column(Integer)

    def __repr__(self):
       return "Paper(name='%s')" % (self.name)

    def __init__(self, name, year):
        self.name = name
        self.year = year
