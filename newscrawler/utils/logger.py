
import logging


def __get_stream_handler(formatter):
    stream_hander = logging.StreamHandler()
    stream_hander.setLevel(logging.DEBUG)
    stream_hander.setFormatter(formatter)
    return stream_hander


def get_logger(name):
    logger = logging.getLogger(name)
    if len(logger.handlers) > 0:
        return logger

    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(name)s %(message)s')
    stream_hander = __get_stream_handler(formatter)
    logger.addHandler(stream_hander)
    return logger