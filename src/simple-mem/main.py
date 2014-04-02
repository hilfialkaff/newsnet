import time
from models import *

DATA_FOLDER = "../../data/"
AUTHOR_PAPER_FILE = "author_paper.txt"
AUTHOR_FILE = "authors.txt"
CITATION_FILE = "citations.txt"
PAPER_FILE = "papers.txt"
PAPER_TERM_FILE = "paper_term.txt"
TERM_FILE = "terms.txt"
VENUE_FILE = "venues.txt"

authors = []
papers = []
terms = []
venues = []

def bootstrap():
    t0 = time.time()
    print "Bootstrapping data..."

    with open(DATA_FOLDER + AUTHOR_FILE) as f:
        for line in f:
            name = line.strip('\n').split('\t')[1]
            authors.append(Author(name))

    with open(DATA_FOLDER + VENUE_FILE) as f:
        for line in f:
            name = line.strip('\n').split('\t')[1]
            venues.append(Venue(name))

    with open(DATA_FOLDER + PAPER_FILE) as f:
        for line in f:
            vals = line.strip('\n').split('\t')
            paper_id = vals[0]
            name = vals[1]
            venue_id = int(vals[2])
            year = vals[3]

            papers.append(Paper(name, year))
            venues[venue_id].add_paper(paper_id)

    with open(DATA_FOLDER + TERM_FILE) as f:
        for line in f:
            name = line.strip('\n').split('\t')[1]
            terms.append(Term(name))

    with open(DATA_FOLDER + PAPER_TERM_FILE) as f:
        for line in f:
            _line = line.strip('\n').split('\t')
            paper_id = int(_line[0])
            term_id = int(_line[1])

            papers[paper_id].add_term(term_id)

    with open(DATA_FOLDER + AUTHOR_PAPER_FILE) as f:
        for line in f:
            _line = line.strip('\n').split('\t')
            author_id = int(_line[0])
            paper_id = int(_line[1])

            authors[author_id].add_paper(paper_id)

    with open(DATA_FOLDER + CITATION_FILE) as f:
        for line in f:
            _line = line.strip('\n').split('\t')
            cites_id = int(_line[0]) + 1
            cited_id = int(_line[1]) + 1


    print "Time taken: ", time.time() - t0

def main():
    bootstrap()

if __name__ == '__main__':
    main()
