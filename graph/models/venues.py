from py2neo import node, rel
from connection import *
from utils.graphlog import *

class Venues(object):
    DATA_PATH = '../../data/venues.txt'


    @staticmethod
    def populate():
        """
        Clears the nodes with label Venue.
        Reads venues.txt and adds them into the graph database.
        """
        Venues.clear()
        batch = neo4j.WriteBatch(newsnet_db)
        #logger.info("Venues - testing hello world")
        with open(Venues.DATA_PATH, 'r') as f:
            for line in f:
                [vid, vname] = line.strip().split('\t')
                venue = batch.create(node({'name': vname}))
                batch.add_labels(venue, "Venue")
        batch.submit()

    @staticmethod
    def clear():
        nodes = newsnet_db.find("Venue")
        batch = neo4j.WriteBatch(newsnet_db)
        for n in nodes:
            batch.delete(n)
        batch.submit()
