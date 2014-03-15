from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

from application import Base, engine
from models import *
import argparse

DATA_FOLDER = "../data/"
AUTHOR_PAPER_FILE = "author_paper.txt"
AUTHOR_FILE = "authors.txt"
CITATION_FILE = "citations.txt"
PAPER_FILE = "papers.txt"
PAPER_TERM_FILE = "paper_term.txt"
TERM_FILE = "terms.txt"
VENUE_FILE = "venues.txt"
BATCH_SIZE = 100000

def init():
    engine.raw_connection().connection.text_factory = str
    Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    return session

def check_commit(session):
    if check_commit.count == BATCH_SIZE:
        print "Committing..."
        session.commit()
        check_commit.count = 0
    else:
        check_commit.count += 1

def insert(session):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    check_commit.count = 0
    """
    with open(DATA_FOLDER + AUTHOR_FILE) as f:
        for line in f:
            name = line.strip('\n').split('\t')[1]
            session.add(Author(name))

            check_commit(session)
    session.commit()

    """

    with open(DATA_FOLDER + VENUE_FILE) as f:
        for line in f:
            name = line.strip('\n').split('\t')[1]
            session.add(Venue(name))

            check_commit(session)
    session.commit()

    with open(DATA_FOLDER + PAPER_FILE) as f:
        for line in f:
            vals = line.strip('\n').split('\t')
            name = vals[1]
            venue_id = int(vals[2]) + 1
            year = vals[3]

            venue = session.query(Venue).filter_by(venue_id=venue_id).first()
            new_paper = Paper(name, year)
            venue.papers.append(new_paper)

            session.add(new_paper)
            session.add(venue)

            check_commit(session)
    session.commit()

    with open(DATA_FOLDER + TERM_FILE) as f:
        for line in f:
            name = line.strip('\n').split('\t')[1]
            session.add(Term(name))

            check_commit(session)
    session.commit()

    with open(DATA_FOLDER + PAPER_TERM_FILE) as f:
        for line in f:
            _line = line.strip('\n').split('\t')
            paper_id = int(_line[0]) + 1
            term_id = int(_line[1]) + 1

            paper = session.query(Paper).filter_by(paper_id=paper_id).first()
            term = session.query(Term).filter_by(term_id=term_id).first()
            paper.terms.append(term)
            session.add(paper)

            check_commit(session)
    session.commit()

    """
    with open(DATA_FOLDER + AUTHOR_PAPER_FILE) as f:
        for line in f:
            _line = line.strip('\n').split('\t')
            author_id = int(_line[0]) + 1
            paper_id = int(_line[1]) + 1

            author = session.query(Author).filter_by(author_id=author_id).first()
            paper = session.query(Paper).filter_by(paper_id=paper_id).first()
            author.papers.append(paper)
            session.add(author)

            check_commit(session)
    session.commit()

    with open(DATA_FOLDER + CITATION_FILE) as f:
        for line in f:
            _line = line.strip('\n').split('\t')
            cites_id = int(_line[0]) + 1
            cited_id = int(_line[1]) + 1
            session.add(Citation(cites_id, cited_id))

            check_commit(session)
    session.commit()
    """

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fresh", help="Insert new data")
    args = parser.parse_args()

    session = init()

    if args.fresh:
        insert(session)

if __name__ == '__main__':
    main()
