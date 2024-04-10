from functools import wraps
from time import time
from loguru import logger


def timing(f):
    @wraps(f)
    def timer(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        logger.info(f'Method: {f.__name__} took: {te - ts:.3f} seconds')
        return result

    return timer
