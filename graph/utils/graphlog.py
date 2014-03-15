import logging

logger = logging.getLogger('graph-newsnet')
hdlr = logging.FileHandler('/var/tmp/graph-newsnet.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)
