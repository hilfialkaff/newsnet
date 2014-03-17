from py2neo import neo4j

newsnet_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
BATCH_SIZE = 20000
