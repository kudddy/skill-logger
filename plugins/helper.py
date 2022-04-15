import time
import logging

# try:
from .config import setting
# except Exception as e:
#     from plugins.config import setting


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)


def timing(f):
    def wrap(*args, **kwargs):
        start = time.time()
        ret = f(*args, **kwargs)
        end = time.time()
        log.debug('{:s} function took {:.3f} ms'.format(f.__name__, (end - start) * 1000.0))
        return ret

    return wrap


def is_true(val):
    if val:
        return val
