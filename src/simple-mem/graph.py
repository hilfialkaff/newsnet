from copy import deepcopy
from node import Node

class Graph:
    def __init__(self):
        self._nodes = {}

    def add_node(self, node):
        if (node.get_type(), node.get_id()) in self._nodes:
            print "! Adding the same node twice"
            return

        self._nodes[(node.get_type(), node.get_id())] = node

    def get_node(self, type, id):
        if (type, id) not in self._nodes:
            # print "(%s, %s) does not exist in graph" % (type, id)
            return None

        return self._nodes[(type, id)]

    def get_nodes(self):
        return self._nodes.values()

    def delete(self, node):
        key = (node.get_type(), node.get_id())

        if key in self._nodes:
            del self._nodes[key]
        else:
            print "Node %s does not exist" % (node)

    def copy(self):
        new_graph = Graph()

        for node in self._nodes.values():
            new_node = Node(node.get_type(), node.get_id(), node.get_info())
            new_node.set_meta_paths(node.get_all_meta_paths())
            new_node.add_categories(deepcopy(node.get_categories()))
            new_graph.add_node(new_node)

        for node in self._nodes.values():
            new_graph_node = new_graph.get_node(node.get_type(), node.get_id())

            for neighbor in node.get_neighbors():
                new_graph_neighbor = new_graph.get_node(neighbor.get_type(), neighbor.get_id())
                new_graph_node.add_neighbor(new_graph_neighbor)

        return new_graph
