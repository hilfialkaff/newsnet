from sqlalchemy import Column, Integer
from application import Base

class Citation(Base):
    __tablename__ = 'citations'

    citation_id = Column(Integer, primary_key=True)
    cites_id = Column(Integer)
    cited_id = Column(Integer)

    def __init__(self, cites_id, cited_id):
        self.cites_id = cites_id
        self.cited_id = cited_id
