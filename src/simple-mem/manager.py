from collections import deque
from node import Node
from forest import Forest

SHELL_PROMPT = "Command: "
CMDS = ["quit", "similarity", "drill-down", "roll-up", "slice", "restore", "display"]
[QUIT, SIMILARITY, DRILL_DOWN, ROLL_UP, SLICE, RESTORE, DISPLAY] = range(0, len(CMDS))

class Manager:
    MAX_PATH_LENGTH = 5
    TOP_K = 50 # Top k-path we are interested

    def __init__(self, graph):
        self._orig_graph = graph
        self._cur_graph = self._orig_graph.copy()
        self._forest = Forest()
        self._subgraph = {} # { category id: { category name: [ node id ]}}
        self._version = 0
        self._deleted_nodes = set()

        self.build_subgraphs(graph)

    def build_subgraphs(self, graph):
        for node in graph.get_nodes():
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

            if cmd == CMDS[QUIT]:
                break

            elif cmd == CMDS[SIMILARITY]:
                [id1, id2] = line.split()[1:]

                if id1 in self._deleted_nodes:
                    print "Node %s doesn't exist in current sub-graph" % (id1)
                    continue

                if id2 in self._deleted_nodes:
                    print "Node %s doesn't exist in current sub-graph" % (id2)
                    continue

                print "Score: ", self.compute_similarity(id1, id2)

            elif cmd == CMDS[DRILL_DOWN]:
                [name, val] = line.split()[1:]

                for node in self._cur_graph.get_nodes():
                    # print name, val, node.get_category(name)
                    category = node.get_category(name)
                    if category and not self._forest.is_member(name, val, category):
                        self._deleted_nodes.add(node.get_id())

                self._version += 1

            elif cmd == CMDS[SLICE]:
                [name, val] = line.split()[1:]
                to_delete = []

                for node in self._cur_graph.get_nodes():
                    if not self._forest.is_slice(name, val, node.get_category(name)):
                        to_delete.append(node)

                for node in to_delete:
                    self._cur_graph.delete(node)

            elif cmd == CMDS[ROLL_UP]:
                [name, val] = line.split()[1:]

                for category_value in self._subgraph[name].keys():
                    if not self._forest.is_member(name, val, category_value):
                        continue

                    for node_id in self._subgraph[name][category_value]:
                        if node_id in self._deleted_nodes:
                            self._deleted_nodes.remove(node_id)

                self._version += 1

            elif cmd == CMDS[RESTORE]:
                to_delete = []

                for node in self._cur_graph.get_nodes():
                    to_delete.append(node)

                for node in to_delete:
                    self._cur_graph.delete(node)

                self._cur_graph = self._orig_graph.copy()

            elif cmd == "print_nodes":
                for node in self._cur_graph.get_nodes():
                    if node.get_id() not in self._deleted_nodes:
                        print node

            elif cmd == "print_num_nodes":
                print "Number of nodes: %d " % \
                    (len(self._cur_graph.get_nodes()) - len(self._deleted_nodes))

            elif cmd == "print_neighbors":
                node_id = line.split()[1]
                node = self._cur_graph.get_node(node_id)

                if node is None:
                    print "Node %s doesn't exist" % (node)
                else:
                    print "Node %s's neighbors" % (node)
                    for neighbor in node.get_neighbors():
                        print "--> %s" % (neighbor)

            elif cmd == "print_meta_paths":
                [id1, id2] = line.split()[1:]
                node1 = self._cur_graph.get_node(id1)
                node2 = self._cur_graph.get_node(id2)

                if id1 in self._deleted_nodes or node1 is None:
                    print "Node %s doesn't exist" % (id1)
                    continue
                if id2 in self._deleted_nodes or node2 is None:
                    print "Node %s doesn't exist" % (id2)
                    continue

                node1.print_meta_paths(id2)

            elif cmd == "search_node":
                node_id = line.split()[1]
                node = self._cur_graph.get_node(node_id)

                if node_id in self._deleted_nodes or node is None:
                    print "Node %s doesn't exist" % (node_id)
                else:
                    print "Node %s exists" % (node)

            else:
                print "Invalid command:", cmd

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

            for neighbor in last_node.get_neighbors().values():
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

        # print paths
        return paths

    # TODO: Better weight assigning
    def compute_score(self, meta_paths):
        score = 0
        for path in meta_paths:
            score += float(1)/len(path)

        return score

    # bfs to the rescue
    def compute_similarity(self, id1, id2):
        node1 = self._cur_graph.get_node(id1)
        node2 = self._cur_graph.get_node(id2)

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
