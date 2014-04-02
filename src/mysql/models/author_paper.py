from sqlalchemy import Column, Integer, String, Table
from application import Base

class AuthorPaper(Base):
    __tablename__ = 'authors-papers'

    author_paper_id = Column(Integer, primary_key=True)
    author_id = Column(Integer)
    paper_id = Column(Integer)

    def __init__(self, author_id, paper_id):
        self.author_id = author_id
        self.paper_id = paper_id
