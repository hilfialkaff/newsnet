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
        return "(%s, %s)" % (self._type, self._id)

    def __eq__(self, other):
        return (self._type == other._type and self._id == other._id)

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
        if (node.get_type(), node.get_id()) in self._neighbors:
            print "! Adding the same neighbor twice"
            return

        self._neighbors[(node.get_type(), node.get_id())] = node

    def get_neighbor(self, type, id):
        if (type, id) not in self._neighbors:
            # print "(%s, %s) does not exist as neighbor of (%s, %s)" % \
            #     (type, id, self._type, self._id)
            return None

        return self._neighbors[(type, id)]

    def get_neighbors(self):
        return self._neighbors.values()

    def get_meta_paths(self, type, id):
        if (type, id) not in self._meta_paths:
            # print "(%s, %s): Metapath to (%s, %s) has not existed yet" % \
            #     (self._type, self._id, type, id)
            return None

        return self._meta_paths[(type, id)]

    def get_all_meta_paths(self):
        return deepcopy(self._meta_paths)

    def add_meta_paths(self, type, id, paths):
        self._meta_paths[(type, id)] = paths

    def set_meta_paths(self, meta_paths):
        self._meta_paths = meta_paths
