from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.orm import relationship, backref
from application import Base
from author_paper import authors_papers_table

class Author(Base):
    __tablename__ = 'authors'

    author_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    papers = relationship("Paper",
                    secondary=authors_papers_table,
                    backref="authors")

    def __repr__(self):
       return "Author(name='%s')" % (self.name)

    def __init__(self, name):
        self.name = name
