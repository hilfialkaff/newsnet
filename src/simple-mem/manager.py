from collections import deque
from node import Node
from forest import Forest

SHELL_PROMPT = "Command: "
CMDS = ["quit", "search", "drill-down", "roll-up", "slice", "restore"]
[QUIT, SEARCH, DRILL_DOWN, ROLL_UP, SLICE, RESTORE] = range(0, len(CMDS))

class Manager:
    MAX_PATH_LENGTH = 5
    TOP_K = 50 # Top k-path we are interested

    def __init__(self, graph):
        self._orig_graph = graph
        self._cur_graph = self._orig_graph.copy()
        self._forest = Forest()

    def shell(self):
        line = raw_input(SHELL_PROMPT)

        while True:
            cmd = line.split()[0]

            if cmd == CMDS[QUIT]:
                break

            elif cmd == CMDS[SEARCH]:
                [type1, id1, type2, id2] = line.split()[1:]
                print "Score: ", self.compute_similarity(type1, id1, type2, id2)

            elif cmd == CMDS[DRILL_DOWN]:
                [name, val] = line.split()[1:]
                to_delete = []

                for node in self._cur_graph.get_nodes():
                    # print name, val, node.get_category(name)
                    category = node.get_category(name)
                    if category and not self._forest.is_member(name, val, category):
                        to_delete.append(node)

                for node in to_delete:
                    self._cur_graph.delete(node)

                print "Nodes left:", len(self._cur_graph.get_nodes())

            elif cmd == CMDS[SLICE]:
                [name, val] = line.split()[1:]
                to_delete = []

                for node in self._cur_graph.get_nodes():
                    if not self._forest.is_slice(name, val, node.get_category(name)):
                        to_delete.append(node)

                for node in to_delete:
                    self._cur_graph.delete(node)

            elif cmd == CMDS[RESTORE]:
                to_delete = []

                for node in self._cur_graph.get_nodes():
                    to_delete.append(node)

                for node in to_delete:
                    self._cur_graph.delete(node)

                self._cur_graph = self._orig_graph.copy()

            else:
                print "Invalid command:", cmd

            line = raw_input(SHELL_PROMPT)

    def test(self):
        print "Similarity: ", self.compute_similarity("author", "42165", "author", "42167")
        print "Similarity: ", self.compute_similarity("author", "42675", "author", "42677")

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

            for neighbor in last_node.get_neighbors():
                new_path = cur_path[:] + [neighbor]

                if not self.is_path_valid(new_path):
                    continue

                if neighbor == dst:
                    paths.append(new_path)
                elif neighbor in cur_path:
                    continue
                else:
                    queue.append(new_path)

        # print paths
        return paths

    # TODO: Better weight assigning?
    def compute_score(self, meta_paths):
        score = 0
        for path in meta_paths:
            score += float(1)/len(path)

        return score

    # bfs to the rescue
    def compute_similarity(self, type1, id1, type2, id2):
        node1 = self._cur_graph.get_node(type1, id1)
        node2 = self._cur_graph.get_node(type2, id2)

        node1_node1_path = node1.get_meta_paths(type1, id1)
        node2_node2_path = node2.get_meta_paths(type2, id2)
        node1_node2_path = node1.get_meta_paths(type2, id2)

        if node1_node1_path == None:
            paths = self.find_path(node1, node1)
            node1.add_meta_paths(type1, id1, paths)

        if node2_node2_path == None:
            paths = self.find_path(node2, node2)
            node2.add_meta_paths(type2, id2, paths)

        if node2_node2_path == None:
            paths = self.find_path(node1, node2)
            node1.add_meta_paths(type2, id2, paths)
            node2.add_meta_paths(type1, id1, paths)

        node1_node1_score = self.compute_score(node1.get_meta_paths(type1, id1))
        node2_node2_score = self.compute_score(node2.get_meta_paths(type2, id2))
        node1_node2_score = self.compute_score(node1.get_meta_paths(type2, id2))

        # print node1_node1_score, node2_node2_score, node1_node2_score
        score = 2 * node1_node2_score / (node1_node1_score + node2_node2_score)

        return score
