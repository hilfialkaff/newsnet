import argparse
import time
from node import Node
import cPickle as pickle
import sys
from collections import deque

DATA_FOLDER = "../../data/"
AUTHOR_PAPER_FILE = "author_paper.txt"
AUTHOR_FILE = "authors.txt"
CITATION_FILE = "citations.txt"
PAPER_FILE = "papers.txt"
PAPER_TERM_FILE = "paper_term.txt"
TERM_FILE = "terms.txt"
VENUE_FILE = "venues.txt"
PICKLE_FILE = "data.p"
MAX_PATH_LENGTH = 5
TOP_K = 1000 # Top k-path we are interested

authors = []
papers = []
terms = []
venues = []

# Store graph of entities. Root will be connected to all entities
root = Node("root", 0)

def bootstrap():
    print "Parsing author file..."
    with open(DATA_FOLDER + AUTHOR_FILE) as f:
        for line in f:
            [id, name] = line.strip('\n').split('\t')
            new_author = Node(Node.AUTHOR_TYPE, id, name)

            root.add_neighbor(new_author)

    print "Parsing venue file..."
    with open(DATA_FOLDER + VENUE_FILE) as f:
        for line in f:
            [id, name] = line.strip('\n').split('\t')
            new_venue = Node(Node.VENUE_TYPE, id, name)

            root.add_neighbor(new_venue)

    print "Parsing paper file..."
    with open(DATA_FOLDER + PAPER_FILE) as f:
        for line in f:
            [id, name, venue_id, year] = line.strip('\n').split('\t')
            new_paper = Node(Node.PAPER_TYPE, id, name, year)
            venue = root.get_neighbor(Node.VENUE_TYPE, venue_id)

            root.add_neighbor(new_paper)
            venue.add_neighbor(new_paper)
            new_paper.add_neighbor(venue)

    print "Parsing term file..."
    with open(DATA_FOLDER + TERM_FILE) as f:
        for line in f:
            [id, name] = line.strip('\n').split('\t')
            new_term = Node(Node.TERM_TYPE, id, name)

            root.add_neighbor(new_term)

    print "Parsing paper term file..."
    with open(DATA_FOLDER + PAPER_TERM_FILE) as f:
        count = 0
        for line in f:
            [paper_id, term_id] = line.strip('\n\r').split('\t')

            paper = root.get_neighbor(Node.PAPER_TYPE, paper_id)
            term = root.get_neighbor(Node.TERM_TYPE, term_id)

            paper.add_neighbor(term)
            term.add_neighbor(paper)

    print "Parsing author paper file..."
    with open(DATA_FOLDER + AUTHOR_PAPER_FILE) as f:
        for line in f:
            [author_id, paper_id] = line.strip('\n\r').split('\t')
            author = root.get_neighbor(Node.AUTHOR_TYPE, author_id)
            paper = root.get_neighbor(Node.PAPER_TYPE, paper_id)

            author.add_neighbor(paper)
            paper.add_neighbor(author)

    print "Parsing citation file..."
    with open(DATA_FOLDER + CITATION_FILE) as f:
        for line in f:
            [citing_paper_id, cited_paper_id] = line.strip('\n\r').split('\t')
            citing_paper = root.get_neighbor(Node.PAPER_TYPE, citing_paper_id)
            cited_paper = root.get_neighbor(Node.PAPER_TYPE, cited_paper_id)

            citing_paper.add_neighbor(cited_paper, Node.CITES_LINK_TYPE)
            cited_paper.add_neighbor(citing_paper, Node.CITED_BY_LINK_TYPE)

    # pickle.dump(root, open(DATA_FOLDER + PICKLE_FILE, "wb"))

def find_path(node1, node2):
    queue = deque()
    paths = []

    queue.append([node1])
    while len(queue) > 0:
        cur_path = queue.popleft()
        last_node = cur_path[-1]

        # Prune this path
        if len(cur_path) == MAX_PATH_LENGTH:
            continue

        # Got the top-k paths
        if len(paths) == TOP_K:
            break

        for neighbor in last_node.get_neighbors():
            new_path = cur_path[:] + [neighbor]

            if neighbor.get_id() == node2.get_id() and neighbor.get_type() == node2.get_type():
                paths.append(new_path)
            elif neighbor in cur_path:
                continue
            else:
                queue.append(new_path)

    # print paths
    return paths

# TODO: Better weight assigning?
def compute_score(meta_paths):
    score = 0
    for path in meta_paths:
        score += float(1)/len(path)

    return score

# bfs to the rescue
def compute_similarity(type1, id1, type2, id2):
    node1 = root.get_neighbor(type1, id1)
    node2 = root.get_neighbor(type2, id2)

    node1_node1_path = node1.get_meta_paths(type1, id1)
    node2_node2_path = node2.get_meta_paths(type2, id2)
    node1_node2_path = node1.get_meta_paths(type2, id2)

    if node1_node1_path == None:
        paths = find_path(node1, node1)
        node1.add_meta_paths(type1, id1, paths)

    if node2_node2_path == None:
        paths = find_path(node2, node2)
        node2.add_meta_paths(type2, id2, paths)

    if node2_node2_path == None:
        paths = find_path(node1, node2)
        node1.add_meta_paths(type2, id2, paths)
        node2.add_meta_paths(type1, id1, paths)

    node1_node1_score = compute_score(node1.get_meta_paths(type1, id1))
    node2_node2_score = compute_score(node2.get_meta_paths(type2, id2))
    node1_node2_score = compute_score(node1.get_meta_paths(type2, id2))

    print node1_node1_score, node2_node2_score, node1_node2_score
    score = 2 * node1_node2_score / (node1_node1_score + node2_node2_score)

    return score

def shell():
    cmd = raw_input("Similarity search> ")

    while cmd != "quit":
        [type1, id1, type2, id2] = cmd.split(',')
        print type1, id1, type2, id2

        print "Score: ", compute_similarity(type1, id1, type2, id2)
        cmd = raw_input("Similarity search> ")

def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--pickle_it", help="Pickle the data", action='store_true')
    # args = parser.parse_args()

    # if args.pickle_it:
    #     bootstrap()

    # root = pickle.load(root, open(DATA_FOLDER + PICKLE_FILE, "wb"))

    bootstrap()
    shell()

if __name__ == '__main__':
    main()
