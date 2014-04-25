import argparse
import yaml

from graph import Graph
from node import Node
from manager import Manager

CONFIG_NAME = 'config.yaml'

def bootstrap():
    graph = Graph()
    config = yaml.load(open(CONFIG_NAME))

    for fname in config['nodes'].values():
        node_type = fname.split('/')[-1][:-len(".txt")]

        with open(fname) as f:
            for line in f:
                [id, name] = line.strip().split('\t')
                new_node = Node(node_type, id, name)

                graph.add_node(new_node)

    for fname in config['relations'].values():
        with open(fname) as f:
            for line in f:
                [node1_id, node2_id, _] = line.strip().split('\t')

                node1 = graph.get_node(node1_id)
                node2 = graph.get_node(node2_id)

                if not node1 or not node2:
                    continue

                node1.add_neighbor(node2)
                node2.add_neighbor(node1)

    for fname in config['maps'].values():
        with open(fname) as f:
            category_name = fname.split('/')[-1][:-len(".map")]

            for line in f:
                [node_id, val] = line.strip().split()
                node = graph.get_node(node_id)
                node.add_category(category_name, val)

    return graph

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--do_test", help="Only test", action='store_true')
    args = parser.parse_args()

    graph = bootstrap()
    # manager = Manager(graph)

    # if args.do_test:
    #     manager.test()
    # else:
    #     manager.shell()

if __name__ == '__main__':
    main()
