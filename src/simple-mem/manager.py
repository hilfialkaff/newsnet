from collections import deque
from node import Node
from forest import Forest
import sys

SHELL_PROMPT = "Command: "
CMDS = ["quit", "similarity", "drill_down", "roll_up", "restore", "display", \
    "print_nodes", "print_num_nodes", "print_neighbors", "print_meta_paths", \
    "search_node", "print_network_statistics", "rank"]

class Manager:
    MAX_PATH_LENGTH = 5
    TOP_K = 50 # Top k-path we are interested

    def __init__(self, graph):
        self._graph = graph
        self._forest = Forest()
        self._subgraph = {} # { category id: { category name: [ node id ]}}
        self._version = 0
        self._deleted_nodes = set()

        self.build_subgraphs()

    def build_subgraphs(self):
        for node in self._graph.get_nodes():
            for name, val in node.get_categories().items():
                if name not in self._subgraph:
                    self._subgraph[name] = {}
                if val not in self._subgraph[name]:
                    self._subgraph[name][val] = []

                self._subgraph[name][val].append(node.get_id())

    def shell(self):
        while True:
            line = raw_input(SHELL_PROMPT)
            cmd = line.split()[0]

            if cmd not in CMDS:
                print "Invalid command:", cmd

            eval("self." + cmd)(line.split()[1:])

    def quit(self, line):
        sys.exit(0)

    def similarity(self, _):
        [id1, id2] = _

        if id1 in self._deleted_nodes:
            print "Node %s doesn't exist in current sub-graph" % (id1)
            return

        if id2 in self._deleted_nodes:
            print "Node %s doesn't exist in current sub-graph" % (id2)
            return

        print "Score: ", self.compute_similarity(id1, id2)

    def drill_down(self, _):
        [name, val] = _

        for node in self._graph.get_nodes():
            # print name, val, node.get_category(name)
            category = node.get_category(name)
            if category and not self._forest.is_member(name, val, category):
                self._deleted_nodes.add(node.get_id())

        self._version += 1

    def roll_up(self, _):
        [name, val] = _

        for category_value in self._subgraph[name].keys():
            if not self._forest.is_member(name, val, category_value):
                return

            for node_id in self._subgraph[name][category_value]:
                if node_id in self._deleted_nodes:
                    self._deleted_nodes.remove(node_id)

        self._version += 1

    def restore(self, _):
        to_delete = []

        for node in self._graph.get_nodes():
            to_delete.append(node)

        for node in to_delete:
            self._graph.delete(node)

        self._graph = self._orig_graph.copy()

    def print_nodes(self, _):
        for node in self._graph.get_nodes():
            if node.get_id() not in self._deleted_nodes:
                print node

    def print_num_nodes(self, _):
        print "Number of nodes: %d " % \
            (len(self._graph.get_nodes()) - len(self._deleted_nodes))

    def print_neighbors(self, _):
        node_id = line.split()[1]
        node = self._graph.get_node(node_id)

        if node is None:
            print "Node %s doesn't exist" % (node)
        else:
            print "Node %s's neighbors" % (node)
            for neighbor in self.get_neighbors(node):
                print "--> %s" % (neighbor)

    def print_meta_paths(self, _):
        [id1, id2] = _
        node1 = self._graph.get_node(id1)
        node2 = self._graph.get_node(id2)

        if id1 in self._deleted_nodes or node1 is None:
            print "Node %s doesn't exist" % (id1)
            return
        if id2 in self._deleted_nodes or node2 is None:
            print "Node %s doesn't exist" % (id2)
            return

        node1.print_meta_paths(id2)

    def search_node(self, _):
        node_id = _[0]
        node = self._graph.get_node(node_id)

        if node_id in self._deleted_nodes or node is None:
            print "Node %s doesn't exist" % (node_id)
        else:
            print "Node %s exists" % (node)

    def print_network_statistics(self, _):
        def stddev(l):
            import math

            mean = sum(l)/len(l)
            return math.sqrt(sum([_ in mean for _ in l])/len(l))

        def print_degree():
            degrees = []

            for node in self._graph.get_nodes():
                degrees.append(len(self.get_neighbors(node)))

            print "- Degree of node avg: %d stddev: %f" % \
                (float(sum(degrees))/len(degrees), stddev(degrees))

        def print_clustering_coeff():
            clustering_coeff = []

            for node in self._graph.get_nodes():
                neighbors = self.get_neighbors(node)
                neighbors_id = set([node.get_id() for node in neighbors])
                count = 0
                num_neighbors = len(neighbors) if len(neighbors) else 1

                for neighbor in neighbors:
                    _neighbors = self.get_neighbors(node)
                    for _neighbor in _neighbors:
                        if _neighbor.get_id() in neighbors_id:
                            count += 1

                clustering_coeff.append(float(count)/num_neighbors)

            print "- Clustering coefficient avg: %d stddev: %f" % \
                (float(sum(clustering_coeff))/len(clustering_coeff), stddev(clustering_coeff))

        print_degree()
        print_clustering_coeff()

    def test_nyc(self):
        print "Similarity: ", self.compute_similarity("0", "3420")

    def test_dblp(self):
        print "Similarity: ", self.compute_similarity("42675", "42677")

    def test(self):
        print "Computing similarity..."
        # self.test_nyc()
        self.test_dblp()

    def is_path_valid(self, path):
        d = {}
        ret = True

        for node in path:
            node_type = node.get_type()

            if node_type in d:
                d[node_type] += 1

                # Only pass a node type twice at most
                if d[node_type] > 2:
                    ret = False
                    break
            else:
                d[node_type] = 1

        return ret

    def find_path(self, src, dst):
        queue = deque()
        paths = []

        queue.append([src])
        while len(queue) > 0:
            cur_path = queue.popleft()
            last_node = cur_path[-1]

            if len(cur_path) == self.MAX_PATH_LENGTH:
                continue

            if len(paths) == self.TOP_K:
                break

            for neighbor in self.get_neighbors(last_node).values():
                if neighbor.get_id() in self._deleted_nodes:
                    continue

                new_path = cur_path[:] + [neighbor]

                # if not self.is_path_valid(new_path):
                #     continue

                if neighbor == dst:
                    paths.append(new_path)
                elif neighbor in cur_path:
                    continue
                else:
                    queue.append(new_path)

        return paths

    # TODO: Better weight assigning
    def compute_score(self, meta_paths):
        score = 0
        for path in meta_paths:
            score += float(1)/len(path)

        return score

    # bfs to the rescue
    def compute_similarity(self, id1, id2):
        node1 = self._graph.get_node(id1)
        node2 = self._graph.get_node(id2)

        node1_node1_path = node1.get_meta_paths(id1)
        node2_node2_path = node2.get_meta_paths(id2)
        node1_node2_path = node1.get_meta_paths(id2)

        if node1_node1_path == None or node1_node1_path[1] < self._version:
            paths = self.find_path(node1, node1)
            node1.add_meta_paths(id1, paths, self._version)

        if node2_node2_path == None or node2_node2_path[1] < self._version:
            paths = self.find_path(node2, node2)
            node2.add_meta_paths(id2, paths, self._version)

        if node1_node2_path == None or node1_node2_path[1] < self._version:
            paths = self.find_path(node1, node2)
            node1.add_meta_paths(id2, paths, self._version)
            node2.add_meta_paths(id1, paths, self._version)

        node1_node1_score = self.compute_score(node1.get_meta_paths(id1)[0])
        node2_node2_score = self.compute_score(node2.get_meta_paths(id2)[0])
        node1_node2_score = self.compute_score(node1.get_meta_paths(id2)[0])

        # print node1_node1_score, node2_node2_score, node1_node2_score
        score = 2 * node1_node2_score / (node1_node1_score + node2_node2_score)

        return score

    def get_neighbors(self, node):
        return [n for n in node.get_neighbors().values() if n.get_id() not in self._deleted_nodes]
