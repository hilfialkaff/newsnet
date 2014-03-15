from sqlalchemy import Table, Integer, ForeignKey, Column
from application import Base

authors_papers_table = Table('authors_papers', Base.metadata,
    Column('author_id', Integer, ForeignKey('authors.author_id')),
    Column('paper_id', Integer, ForeignKey('papers.paper_id'))
)
