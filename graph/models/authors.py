from py2neo import node, rel
from connection import *

class Authors(object):
    DATA_PATH = '../../data/authors.txt'

    @staticmethod
    def populate():
        """
        Clears the nodes with label Author.
        Reads authors.txt and adds them into the graph database.
        """
        print "# AUTHORS"
        print "## CLEARING AUTHORS"
        Authors.clear()
        print "## DONE CLEARING AUTHORS"
        print "## ADDING AUTHORS"
        batch = neo4j.WriteBatch(newsnet_db)
        with open(Authors.DATA_PATH, 'r') as f:
            for line in f:
                print line.strip()
                [aid, aname] = line.strip().split('\t')
                author = batch.create(node({'name': aname}))
                batch.add_labels(author, "Author")
        batch.submit()
        print "## DONE ADDING AUTHORS"

    @staticmethod
    def clear():
        nodes = newsnet_db.find("Author")
        batch = neo4j.WriteBatch(newsnet_db)
        for n in nodes:
            batch.delete(n)
        batch.submit()