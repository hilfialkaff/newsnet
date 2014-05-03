class HierarchyTree:

    class TreeNode:
        def __init__(self, nid, name, pid):
            self._nid = nid
            self._name = name
            self._pid = pid
            self._children = []
            self._parent = []

    def __init__(self):
        """
        Create an empty Hierarch tree
        """
        self._names = {}
        self._names['root'] = '0'
        self._tree = {}
        root = self.TreeNode('0', 'root', '0')
        self._tree = {'0': root}


    def _build(self,path):
        # build the tree first
        with open(path, 'r') as f:
            for line in f:
                vals = line.split('\t')
                cid = vals[0].strip()
                cpid = vals[1]
                cname = vals[2].strip()

                if not cid in self._tree:
                    # currently leaf
                    node = self.TreeNode(cid, cname, cpid)
                    self._tree[cid] = node
                else:
                    # was a parent of someone
                    self._tree[cid]._name = cname
                    self._tree[cid]._parent = cpid

                if not cpid in self._tree:
                    self._tree[cpid] = self.TreeNode(cpid, None, None)
                else:
                    parent = self._tree[cpid]
                    parent._children.append(cid)

                # insert into names
                self._names[cname] = cid
            # endfor
        # endwidth
    # end

    # API

    def is_slice(self, name, qid):
        cid = self._names[name]
        return qid == cid

    def is_member(self, name, qid):
        cid = self._names[name]
        stack = []
        stack.append(cid)

        while stack:
            nid = stack.pop()

            if nid == qid:
                return True

            for child in self._tree[nid]._children:
                stack.append(child)
        # endwhile
        return False

    def get_children(self, name):
        result = []
        id = self._names[name]
        children_id = self._tree[id]._children

        for _id in children_id:
            for name, __id in self._names.items():
                if _id == __id:
                    result.append(name)
                    break

        return result

    def get_parent(self, name):
        result = ""
        id = self._names[name]
        parent_id = self._tree[id]._parent

        for name, _id in self._names.items():
            if _id == parent_id:
                result = name
                break

        return result

    def __str__(self):
        s = ""
        stack = []
        stack.append(('0',0))

        while stack :
            (nid, level) = stack.pop()
            s += "|"
            for i in range (0, level):
                s += "____"
            s += " ( " + self._tree[nid]._name + ", " + self._tree[nid]._nid + " )\n"

            for cid in self._tree[nid]._children:
                stack.append( (cid, level + 1) )
        # endwhile
        return s

if __name__== "__main__":
    ht = HierarchyTree()
    ht._build('/Users/efekarakus/Work/NewsNet/newsnet/data/hierarchy_data/area.hier')
    print str(ht)

    print "slicing"
    print ht.is_slice('DB', '2')
    print ht.is_slice('DB', '3')

    print ""

    print "is_member"
    print ht.is_member('root', '2')
    print ht.is_member('DB', '3')
    print ht.is_member('DB', '2')
