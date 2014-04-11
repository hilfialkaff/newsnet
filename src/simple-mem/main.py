import argparse
import time
from node import Node
import cPickle as pickle
import sys
from collections import deque

DATA_FOLDER = "../../data/hierarchy_data/"
AUTHOR_FILE = "author.txt"
PAPER_FILE = "paper.txt"
TERM_FILE = "term.txt"
CONF_FILE = "conf.txt"
RELATION_FILE = "new_relation.txt"
PICKLE_FILE = "data.p"
MAX_PATH_LENGTH = 5
TOP_K = 1000 # Top k-path we are interested

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

def find_path(src, dst):
    queue = deque()
    paths = []

    queue.append([src])
    while len(queue) > 0:
        cur_path = queue.popleft()
        last_node = cur_path[-1]

        if len(cur_path) == MAX_PATH_LENGTH:
            continue

        if len(paths) == TOP_K:
            break

        for neighbor in last_node.get_neighbors():
            new_path = cur_path[:] + [neighbor]

            if neighbor == dst:
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
    # TODO: Find how to use pickle
    bootstrap()
    shell()

if __name__ == '__main__':
    main()
