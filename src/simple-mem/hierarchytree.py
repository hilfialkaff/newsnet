from collections import deque

class HierarchyTree:

    class TreeNode:
        def __init__(self, nid, name, pid):
            self._nid = nid
            self._name = name
            self._pid = pid
            self._children = []

    def __init__(self):
        """
        Create an empty Hierarch tree
        """
        self._tree = {}
        root = self.TreeNode('0', 'root', '0')
        self._tree = {'0': root}


    def _build_tree(self,path):
        # build the tree first
        with open(path, 'r') as f:
            for line in f:
                vals = line.split('\t')
                cid = vals[0].strip()
                cpid = vals[1]
                cname = vals[2].strip()
               
                node = self.TreeNode(cid, cname, cpid)
                self._tree[cid] = node
                
                parent = self._tree[cpid]
                parent._children.append(cid)
                # endfor
            # endwidth
        # end

    def is

    def __str__(self):
        s = ""
        queue = deque([])
        queue.append(('0',0))
        
        while len(queue) > 0:
            (nid, level) = queue.popleft()
            s += "|"
            for i in range (0, level):
                s += "____"
            s += " ( " + self._tree[nid]._name + ", " + self._tree[nid]._nid + " )\n"

            for cid in self._tree[nid]._children:
                queue.append( (cid, level + 1) )
        # endwhile
        return s

if __name__== "__main__":
    ht = HierarchyTree()
    ht._build_tree('/Users/efekarakus/Work/NewsNet/newsnet/data/hierarchy_data/area.hier')
    print str(ht)
