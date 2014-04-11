from node import Node

DATA_FOLDER = "../../data/hierarchy_data/"
AUTHOR_FILE = "author.txt"
PAPER_FILE = "paper.txt"
TERM_FILE = "term.txt"
CONF_FILE = "conf.txt"
RELATION_FILE = "relation.txt"
NEW_RELATION_FILE = "new_relation.txt"

# Store graph of entities. Root will be connected to all entities
root = Node("root", 0)

def main():
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
    with open(DATA_FOLDER + RELATION_FILE) as f, open(DATA_FOLDER + NEW_RELATION_FILE, 'w') as out:
        for line in f:
            [node1_id, node2_id, level] = line.strip('\n').split('\t')
            node1_type = get_node_type(root, node1_id)
            node2_type = get_node_type(root, node2_id)
            out.write(node1_id + '\t' + node1_type + '\t' + node2_id + '\t' + node2_type + '\t' + level + '\n')

def get_node_type(root, node_id):
    ret = None

    if root.get_neighbor(Node.AUTHOR_TYPE, node_id):
        ret = "author"
    elif root.get_neighbor(Node.PAPER_TYPE, node_id):
        ret = "paper"
    elif root.get_neighbor(Node.CONF_TYPE, node_id):
        ret = "conf"
    elif root.get_neighbor(Node.TERM_TYPE, node_id):
        ret = "term"

    return ret

if __name__ == '__main__':
    main()
