from sqlalchemy import Column, Integer, String
from application import Base

class Venue(Base):
    __tablename__ = 'venues'

    venue_id = Column(Integer, primary_key=True)
    name = Column(String(500))

    def __repr__(self):
        return "Venue(name=%s)" % (self.name)

    def __init__(self, name):
        self.name = name
