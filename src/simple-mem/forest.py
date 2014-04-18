from hierarchytree import HierarchyTree

class Forest:

    def __init__(self):
        org = HierarchyTree()
        area = HierarchyTree()

        area._build('../../data/hierarchy_data/area.hier')
        org._build('../../data/hierarchy_data/org.hier')

        self._forest = {
            'area': area,
            'org': org
        }

    def is_member(category, name, qid):
        return self._forest[category].is_member(name, qid)

    def is_slice(category, name, qid):
        return self._forest[category].is_slice(name, qid)

if __name__ == "__main__":
    forest = Forest()
    area = forest._forest['area']
    org = forest._forest['org']

    print str(area)
    print str(org)

    print area.is_member("root", "4")
   
    print org.is_slice("root", "4")
    print org.is_slice("SIAM", "3")
    print org.is_slice("IEEE", "3")
