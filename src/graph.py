from copy import deepcopy
from node import Node

class Graph:
    def __init__(self):
        self._nodes = {}

    def add_node(self, node):
        if node.get_id() in self._nodes:
            print "! Adding the same node twice"
            return

        self._nodes[node.get_id()] = node

    def get_node(self, node_id):
        if node_id not in self._nodes:
            # print "(%s, %s) does not exist in graph" % (type, id)
            return None

        return self._nodes[node_id]

    def get_nodes(self):
        return self._nodes.values()

    def delete(self, node):
        key = node.get_id()

        if key in self._nodes:
            del self._nodes[key]
        else:
            print "Node %s does not exist" % (node)

    def copy(self):
        new_graph = Graph()

        for node in self._nodes.values():
            new_graph.add_node(node.copy())

        for node in self._nodes.values():
            new_graph_node = new_graph.get_node(node.get_id())

            for neighbor in node.get_neighbors().values():
                new_graph_neighbor = new_graph.get_node(neighbor.get_id())
                new_graph_node.add_neighbor(new_graph_neighbor)

        return new_graph
