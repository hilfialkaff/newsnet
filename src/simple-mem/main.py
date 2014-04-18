import argparse
import time
from node import Node
import cPickle as pickle
import sys
from manager import Manager

DATA_FOLDER = "../../data/hierarchy_data/"
AUTHOR_FILE = "author.txt"
PAPER_FILE = "paper.txt"
TERM_FILE = "term.txt"
CONF_FILE = "conf.txt"
RELATION_FILE = "new_relation.txt"
PICKLE_FILE = "data.p"

def bootstrap():
    # Store graph of entities. Root will be connected to all entities
    root = Node("root", 0)

    print "Parsing author file..."
    with open(DATA_FOLDER + AUTHOR_FILE) as f:
        for line in f:
            [id, name] = line.strip('\n').split('\t')
            new_author = Node(Node.AUTHOR_TYPE, id, name)

            root.add_neighbor(new_author)

    print "Parsing venue file..."
    with open(DATA_FOLDER + CONF_FILE) as f:
        for line in f:
            [id, name] = line.strip('\n').split('\t')
            new_conf = Node(Node.CONF_TYPE, id, name)

            root.add_neighbor(new_conf)

    print "Parsing paper file..."
    with open(DATA_FOLDER + PAPER_FILE) as f:
        for line in f:
            [id, name] = line.strip('\n').split('\t')
            new_paper = Node(Node.PAPER_TYPE, id, name)

            root.add_neighbor(new_paper)

    print "Parsing term file..."
    with open(DATA_FOLDER + TERM_FILE) as f:
        for line in f:
            [id, name] = line.strip('\n').split('\t')
            new_term = Node(Node.TERM_TYPE, id, name)

            root.add_neighbor(new_term)

    print "Parsing relation file..."
    with open(DATA_FOLDER + RELATION_FILE) as f:
        for line in f:
            [node1_id, node1_type, node2_id, node2_type, level] = line.strip('\n').split('\t')

            node1 = root.get_neighbor(node1_type, node1_id)
            node2 = root.get_neighbor(node2_type, node2_id)
            node1.add_neighbor(node2)
            node2.add_neighbor(node1)

    return root

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--do_test", help="Only test", action='store_true')
    args = parser.parse_args()

    root = bootstrap()
    manager = Manager(root)

    if args.do_test:
        manager.test()
    else:
        manager.shell()

if __name__ == '__main__':
    main()
