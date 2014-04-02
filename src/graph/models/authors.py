from py2neo import node, rel
from connection import *
from utils.graphlog import *

class Authors(object):
    DATA_PATH = '../data/authors.txt'

    @staticmethod
    def populate():
        """
        Clears the nodes with label Author.
        Reads authors.txt and adds them into the graph database.
        """
        logger.info("AUTHORS: starting clear")
        Authors.clear()
        logger.info("AUTHORS: end clear")
        batch = neo4j.WriteBatch(newsnet_db)

        count = 0
        num_batch = 0
        with open(Authors.DATA_PATH, 'r') as f:
            for line in f:
                vals = line.strip().split('\t')
                if len(vals) <= 1: continue

                aid, aname = vals[0], vals[1]
                author = batch.create(node({'id': aid, 'name': aname}))
                batch.add_labels(author, "Author")
                count += 1

                # submit every BATCH_SIZE
                if count == BATCH_SIZE:
                    batch.run()
                    num_batch += 1
                    logger.info("AUTHORS: submitted batch [%d, %d]" % ((num_batch-1)*BATCH_SIZE, num_batch*BATCH_SIZE))
                    count = 0

        if count > 0:
            batch.run()
        logger.info("AUTHORS: done")

    @staticmethod
    def clear():
        nodes = newsnet_db.find("Author")
        batch = neo4j.WriteBatch(newsnet_db)
        count = 0
        for n in nodes:
            batch.delete(n)
            count += 1
            if count == BATCH_SIZE:
                batch.run()
        if count > 0:
            batch.run()
