from sqlalchemy import Column, Integer, String, Table
from application import Base

class Author(Base):
    __tablename__ = 'authors'

    author_id = Column(Integer, primary_key=True)
    name = Column(String(100))

    def __repr__(self):
       return "Author(name='%s')" % (self.name)

    def __init__(self, name):
        self.name = name
