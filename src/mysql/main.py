from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

from application import Base, engine
from models import *
import argparse
import time

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

def check_commit(table, data):
    ret = True
    if len(data) != BATCH_SIZE:
        ret = False
    else:
        print "Committing..."
        t0 = time.time()
        engine.execute(table.__table__.insert(), data)
        print "Finish committing in:", str(time.time() - t0)

    return ret

def insert(session):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    check_commit.count = 0
    with open(DATA_FOLDER + AUTHOR_FILE) as f:
        data = []
        for line in f:
            name = line.strip('\n').split('\t')[1]

            data.append({"name": name})
            if check_commit(Author, data):
                data = []

    print "Finish author"

    with open(DATA_FOLDER + VENUE_FILE) as f:
        data = []

        for line in f:
            name = line.strip('\n').split('\t')[1]

            data.append({"name": name})
            if check_commit(Venue, data):
                data = []

    print "Finish venue"

    with open(DATA_FOLDER + PAPER_FILE) as f:
        paper_data = []
        venue_paper_data = []
        count = 1

        for line in f:
            vals = line.strip('\n').split('\t')
            name = vals[1]
            venue_id = int(vals[2]) + 1
            year = vals[3]

            paper_data.append({"name": name, "year": year})
            if check_commit(Paper, paper_data):
                paper_data = []

            venue_paper_data.append({"venue_id": venue_id, "paper_id": count})
            if check_commit(VenuePaper, venue_paper_data):
                venue_paper_data = []

            count += 1

    print "Finish paper"

    with open(DATA_FOLDER + TERM_FILE) as f:
        data = []
        for line in f:
            name = line.strip('\n').split('\t')[1]

            data.append({"name": name})
            if check_commit(Term, data):
                data = []

    print "Finish term"

    with open(DATA_FOLDER + PAPER_TERM_FILE) as f:
        data = []
        for line in f:
            _line = line.strip('\n').split('\t')
            paper_id = int(_line[0]) + 1
            term_id = int(_line[1]) + 1

            data.append({"paper_id": paper_id, "term_id": term_id})
            if check_commit(PaperTerm, data):
                data = []

    print "Finish paper term"

    with open(DATA_FOLDER + AUTHOR_PAPER_FILE) as f:
        data = []
        for line in f:
            _line = line.strip('\n').split('\t')
            author_id = int(_line[0]) + 1
            paper_id = int(_line[1]) + 1

            data.append({"author_id": author_id, "paper_id": paper_id})
            if check_commit(AuthorPaper, data):
                data = []

    print "Finish author paper"

    with open(DATA_FOLDER + CITATION_FILE) as f:
        data = []
        for line in f:
            _line = line.strip('\n').split('\t')
            cites_id = int(_line[0]) + 1
            cited_id = int(_line[1]) + 1

            data.append({"cites_id": cites_id, "cited_id": cited_id})
            if check_commit(Citation, data):
                data = []

    print "Finish citation"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fresh", help="Insert new data")
    args = parser.parse_args()

    session = init()

    if args.fresh:
        insert(session)

if __name__ == '__main__':
    main()
