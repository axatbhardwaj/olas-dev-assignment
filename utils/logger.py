import logging


def get_logger(name):
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logger = logging.getLogger(name)
    return logger
