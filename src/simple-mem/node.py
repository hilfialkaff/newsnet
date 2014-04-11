class Node:
    AUTHOR_TYPE = "author"
    PAPER_TYPE = "paper"
    CONF_TYPE = "conf"
    TERM_TYPE = "term"
    CITES_LINK_TYPE = "cites"
    CITED_BY_LINK_TYPE = "cited_by"

    def __init__(self, type, id, *info):
        self._type = type
        self._id = id
        self._info = info
        self._neighbors = {} # key = (type, id), val = Node object
        self._meta_paths = {} # key = (type, id), val = list of paths

    def __repr__(self):
        return "(%s, %s)" % (self._type, self._id)

    def __eq__(self, other):
        return (self._type == other._type and self._id == other._id)

    def get_type(self):
        return self._type

    def get_id(self):
        return self._id

    def add_neighbor(self, node, link_name=""):
        if (node.get_type(), node.get_id()) in self._neighbors:
            print "! Adding the same neighbor twice"
            return

        self._neighbors[(node.get_type(), node.get_id(), link_name)] = node

    def get_neighbor(self, type, id, link_name=""):
        if (type, id, link_name) not in self._neighbors:
            # print "(%s, %s, %s) does not exist as neighbor of (%s, %s)" % \
            #     (type, id, link_name, self._type, self._id)
            return None

        return self._neighbors[(type, id, link_name)]

    def get_neighbors(self):
        return self._neighbors.values()

    def get_meta_paths(self, type, id):
        if (type, id) not in self._meta_paths:
            # print "(%s, %s): Metapath to (%s, %s) has not existed yet" % \
            #     (self._type, self._id, type, id)
            return None

        return self._meta_paths[(type, id)]

    def add_meta_paths(self, type, id, paths):
        self._meta_paths[(type, id)] = paths
