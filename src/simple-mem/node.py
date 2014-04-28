from copy import deepcopy

class Node:
    def __init__(self, type, id, *info):
        self._type = type
        self._id = id
        self._info = info
        self._neighbors = {} # key = (type, id), val = Node object
        self._meta_paths = {} # key = (type, id), val = list of paths
        self._categories = {} # key = category, val = string id

    def __repr__(self):
        return "(%s:%s:%s)" % (self._type, self._id, self._categories)

    def __eq__(self, other):
        return self._id == other._id

    def get_type(self):
        return self._type

    def get_id(self):
        return self._id

    def get_info(self):
        return self._info

    def add_category(self, name, val):
        self._categories[name] = val

    def get_category(self, name):
        if name not in self._categories.keys():
            # print "Name %s does not exist" % (name)
            return None

        return self._categories[name]

    def get_categories(self):
        return self._categories

    def add_categories(self, categories):
        self._categories = categories

    def add_neighbor(self, node):
        if node.get_id() in self._neighbors:
            print "! Adding the same neighbor twice"
            return

        self._neighbors[node.get_id()] = node

    def get_neighbor(self, id):
        if id not in self._neighbors:
            # print "(%s, %s) does not exist as neighbor of (%s, %s)" % \
            #     (type, id, self._type, self._id)
            return None

        return self._neighbors[id]

    def delete_neighbor(self, node):
        key = (node.get_type(), node.get_id())

        if key not in self._neighbors:
            print "%s does not exist as neighbor of (%s, %s)" % \
                (key, self._type, self._id)
            return False
        else:
            del self._neighbors[node.get_id()]
            return True

    def get_neighbors(self):
        return self._neighbors

    def set_neighbors(self, neighbors):
        self._neighbors = neighbors

    def get_meta_paths(self, id):
        if id not in self._meta_paths:
            # print "(%s, %s): Metapath to (%s, %s) has not existed yet" % \
            #     (self._type, self._id, type, id)
            return None

        return self._meta_paths[id]

    def get_all_meta_paths(self):
        return self._meta_paths

    def add_meta_paths(self, id, paths, version):
        self._meta_paths[id] = (paths, version)

    def set_meta_paths(self, meta_paths):
        self._meta_paths = meta_paths

    def print_meta_paths(self, node_id):
        if node_id not in self._meta_paths:
            print "Node %s doesn't exist in meta-path of %s" (node_id, self)
            return

        paths = self._meta_paths[node_id][0]
        for i in range(len(paths)):
            print "Path %d: %s" % (i, paths[i])

    def copy(self):
        new_node = Node(self.get_type(), self.get_id(), self.get_info())
        new_node.set_meta_paths(deepcopy(self.get_all_meta_paths()))
        new_node.add_categories(deepcopy(self.get_categories()))

        return new_node
