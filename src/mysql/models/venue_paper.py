from sqlalchemy import Column, Integer
from application import Base

class VenuePaper(Base):
    __tablename__ = 'venues-papers'

    venue_paper_id = Column(Integer, primary_key=True)
    venue_id = Column(Integer)
    paper_id = Column(Integer)

    def __init__(self, venue_id, paper_id):
        self.venue_id = venue_id
        self.paper_id = paper_id
