import logging

FORMAT = "%(levelname)s \t %(asctime)s \t %(funcName)s \t %(msg)s"

logging.basicConfig(format=FORMAT)
logger = logging.getLogger("Problem")
logger.setLevel("INFO")
