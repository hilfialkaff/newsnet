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
        Authors.clear()
        batch = neo4j.WriteBatch(newsnet_db)
        with open(Authors.DATA_PATH, 'r') as f:
            for line in f:
                [aid, aname] = line.strip().split('\t')
                author = batch.create(node({'name': aname}))
                batch.add_labels(author, "Author")
        batch.submit()

    @staticmethod
    def clear():
        nodes = newsnet_db.find("Author")
        batch = neo4j.WriteBatch(newsnet_db)
        for n in nodes:
            batch.delete(n)
        batch.submit()
