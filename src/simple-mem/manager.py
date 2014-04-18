from node import Node
from collections import deque

SHELL_PROMPT = "Command: "
CMDS = ["quit", "search", "drill-down", "roll-up", "slice"]
[QUIT, SEARCH, DRILL_DOWN, ROLL_UP, SLICE] = range(0, len(CMDS))

class Manager:
    MAX_PATH_LENGTH = 5
    TOP_K = 50 # Top k-path we are interested

    def __init__(self, root):
        self._root = root

    def shell(self):
        line = raw_input(SHELL_PROMPT)

        while True:
            cmd = line.split()[0]

            if cmd == CMDS[QUIT]:
                break
            elif cmd == CMDS[SEARCH]:
                [type1, id1, type2, id2] = line.split()[1:]
                print type1, id1, type2, id2

                print "Score: ", self.compute_similarity(type1, id1, type2, id2)
            elif cmd == CMDS[DRILL_DOWN]:
                pass
            elif cmd == CMDS[ROLL_UP]:
                pass
            elif cmd == CMDS[SLICE]:
                pass
            else:
                print "Invalid command:", cmd

            line = raw_input(SHELL_PROMPT)

    def test(self):
        print "Similarity: ", self.compute_similarity("author", "42165", "author", "42167")

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

        print paths
        return paths

    # TODO: Better weight assigning?
    def compute_score(self, meta_paths):
        score = 0
        for path in meta_paths:
            score += float(1)/len(path)

        return score

    # bfs to the rescue
    def compute_similarity(self, type1, id1, type2, id2):
        node1 = self._root.get_neighbor(type1, id1)
        node2 = self._root.get_neighbor(type2, id2)

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
