from py2neo import node, rel
from connection import *
from utils.graphlog import *

class Venues(object):
    DATA_PATH = '../data/venues.txt'


    @staticmethod
    def populate():
        """
        Clears the nodes with label Venue.
        Reads venues.txt and adds them into the graph database.
        """
        logger.info("VENUES: starting clear")
        Venues.clear()
        logger.info("VENUES: end clear")
        batch = neo4j.WriteBatch(newsnet_db)

        count = 0
        num_batch = 0
        with open(Venues.DATA_PATH, 'r') as f:
            for line in f:
                vals = line.strip().split('\t')
                if len(vals) <= 1: continue

                vid, vname = vals[0], vals[1]
                venue = batch.create(node({'id': vid, 'name': vname}))
                batch.add_labels(venue, "Venue")
                count += 1

                if count == BATCH_SIZE:
                    batch.run()
                    num_batch += 1
                    logger.info("VENUES: submitted batch [%d, %d]" % ((num_batch-1)*BATCH_SIZE, num_batch*BATCH_SIZE))
                    count = 0

        if count > 0:
            batch.run()
        logger.info("VENUES: done")

    @staticmethod
    def clear():
        nodes = newsnet_db.find("Venue")
        batch = neo4j.WriteBatch(newsnet_db)
        count = 0
        for n in nodes:
            batch.delete(n)
            count += 1
            if count == BATCH_SIZE:
                batch.run()
        if count > 0:
            batch.run()
