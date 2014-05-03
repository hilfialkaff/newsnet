from collections import deque
from node import Node
from forest import Forest
import sys
import time
import random
import logging

SHELL_PROMPT = "Command: "
CMDS = ["quit", "similarity", "drill_down", "roll_up", "restore", "rank", \
    "print_nodes", "print_num_nodes", "print_neighbors", "print_meta_paths", \
    "search_node", "print_network_statistics", "print_children", "print_parent", "print_node"]

class Manager:
    MAX_PATH_LENGTH = 5
    TOP_K = 50 # Top k-path we are interested

    def __init__(self, graph):
        self._graph = graph
        self._forest = Forest()
        self._subgraph = {} # { category id: { category name: [ node id ]}}
        self._version = 0
        self._deleted_nodes = set()
        self._current_level = dict([(category, "root") for category in self._forest.get_categories()])

        self.build_subgraphs()
        self.set_logging()

    def set_logging(self):
        logging.basicConfig(filename="result.log", format='%(asctime)-15s %(message)s')
        self._logger = logging.getLogger()

    def build_subgraphs(self):
        for node in self.get_nodes():
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
                continue

            eval("self." + cmd)(line.split()[1:])

    def quit(self, line):
        sys.exit(0)

    def similarity(self, _):
        [id1, id2] = _

        start = time.time()

        if id1 in self._deleted_nodes:
            print "Node %s doesn't exist in current sub-graph" % (id1)
            return

        if id2 in self._deleted_nodes:
            print "Node %s doesn't exist in current sub-graph" % (id2)
            return

        score = self.compute_similarity(id1, id2)
        print "score:", score
        self._logger.warning("Time taken for similarity search: %f" % (time.time() - start))
        self._logger.warning("Score: %s " %(score))

    def drill_down(self, _):
        [name, val] = _

        start = time.time()

        for node in self.get_nodes():
            category = node.get_category(name)
            if category and not self._forest.is_member(name, val, category):
                self._deleted_nodes.add(node.get_id())

        self._logger.warning("Time taken for drill-down: %f" % (time.time() - start))
        # self._logger.warning("deleted nodes: %d" % (len(self._deleted_nodes)))
        # self._logger.warning("deleted nodes: %s" % (self._deleted_nodes))
        self._current_level[name] = val
        self._version += 1

    def roll_up(self, _):
        [name, val] = _

        start = time.time()

        for category_value in self._subgraph[name].keys():
            if not self._forest.is_member(name, val, category_value):
                self._logger.warning("%s %s %s" % (name, val, category_value))
                continue

            for node_id in self._subgraph[name][category_value]:
                if node_id in self._deleted_nodes:
                    self._deleted_nodes.remove(node_id)

        self._logger.warning("Time taken for roll-up: %f" % (time.time() - start))
        # self._logger.warning("deleted nodes: %d" % (len(self._deleted_nodes)))
        # self._logger.warning("deleted nodes: %s" % (self._deleted_nodes))
        self._current_level[name] = val
        self._version += 1

    def restore(self, _):
        to_delete = []

        for node in self.get_nodes():
            to_delete.append(node)

        for node in to_delete:
            self._graph.delete(node)

        self._graph = self._orig_graph.copy()

    def print_node(self, _):
        [node_id] = _

        print self._graph.get_node(node_id)

    def print_nodes(self, _):
        for node in self.get_nodes():
            self._logger.warning(node)

    def print_num_nodes(self, _):
        print "Number of nodes: %d " % (len(self.get_nodes()))

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
            return math.sqrt(float(sum([(_ - mean)**2 for _ in l]))/len(l))

        def print_degree():
            degrees = []

            for node in self.get_nodes():
                degrees.append(len(self.get_neighbors(node)))

            self._logger.warning("- Degree of node avg: %d stddev: %f" % \
                (float(sum(degrees))/len(degrees), stddev(degrees)))

        def print_clustering_coeff():
            clustering_coeff = []

            for node in self.get_nodes():
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

            self._logger.warning("- Clustering coefficient avg: %d stddev: %f" % \
                (float(sum(clustering_coeff))/len(clustering_coeff), stddev(clustering_coeff)))

        print_degree()
        # print_clustering_coeff()

    def print_children(self, _):
        for category, name in self._current_level.items():
            print "Category: %s, name: %s" % (category, name)
            for child in self._forest.get_children(category, name):
                print "- " + child
            print ""

    def print_parent(self, _):
        for category, name in self._current_level.items():
            print "Category: %s, name: %s" % (category, name)
            print "- " + self._forest.get_parent(category, name)
            print ""

    def test_nyt(self):
        self.print_network_statistics([])
        nodes = [node for node in self.get_nodes() if node.get_type() == "article"]

        for _ in range(100):
            self.drill_down(["loctype", "Eurasia"])
            self.drill_down(["loctype", "Jordan"])
            self.roll_up(["loctype", "Eurasia"])
            self.roll_up(["loctype", "root"])

        self.drill_down(["loctype", "Eurasia"])
        self.print_network_statistics([])
        nodes = [node for node in self.get_nodes() if node.get_type() == "article"]

        for _ in range(100):
            node1 = random.choice(nodes)
            node2 = random.choice(nodes)

            while node1 == node2:
                node2 = random.choice(nodes)

            self.similarity([node1.get_id(), node2.get_id()])

    def test_dblp(self):
        self.print_network_statistics([])
        nodes = [node for node in self.get_nodes() if node.get_type() == "author"]

        for _ in range(100):
            node1 = random.choice(nodes)
            node2 = random.choice(nodes)

            while node1 == node2:
                node2 = random.choice(nodes)

            self.similarity([node1.get_id(), node2.get_id()])

        for _ in range(100):
            self.drill_down(["area", "DB"])
            self.roll_up(["area", "root"])

        self.drill_down(["area", "DB"])
        self.print_network_statistics([])
        nodes = [node for node in self.get_nodes() if node.get_type() == "author"]

        for _ in range(100):
            node1 = random.choice(nodes)
            node2 = random.choice(nodes)

            while node1 == node2:
                node2 = random.choice(nodes)

            self.similarity([node1.get_id(), node2.get_id()])

    def test(self):
        print "Computing similarity..."
        self.test_nyt()
        # self.test_dblp()

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

            for neighbor in self.get_neighbors(last_node):
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

    def get_nodes(self):
        return [n for n in self._graph.get_nodes() if n.get_id() not in self._deleted_nodes]
