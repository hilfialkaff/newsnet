from hierarchytree import HierarchyTree
import yaml

class Forest:

    def __init__(self):
        config = yaml.load( open('config.yaml', 'r') )
        self._forest = {}
        hierarchies = config['hierarchies']
        for hierarchy in hierarchies:
            self._forest[hierarchy] = HierarchyTree()
            self._forest[hierarchy]._build( hierarchies[hierarchy] )

        """
        org = HierarchyTree()
        area = HierarchyTree()

        area._build('../../data/hierarchy_data/area.hier')
        org._build('../../data/hierarchy_data/org.hier')

        self._forest = {
            'area': area,
            'org': org
        }
        """

    def is_member(self, category, name, qid):
        return self._forest[category].is_member(name, qid)

    def is_slice(self, category, name, qid):
        return self._forest[category].is_slice(name, qid)

    def get_categories(self):
        return self._forest.keys()

    def get_children(self, category, name):
        return self._forest[category].get_children(name)

    def get_parent(self, category, name):
        return self._forest[category].get_parent(name)

if __name__ == "__main__":
    forest = Forest()
    for hier in forest._forest:
        print forest._forest[hier]
