import logging
from contextlib import contextmanager


def my_function():
    logging.debug('Some debug data')
    logging.error('Some error data')
    logging.debug('More debug data')


@contextmanager
def debug_logging(level):
    logger = logging.getLogger()
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield
    finally:
        logger.setLevel(old_level)


@contextmanager
def log_level(level, name):
    logger = logging.getLogger(name)
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield logger
    finally:
        logger.setLevel(old_level)

if __name__ == '__main__':
    # with debug_logging(logging.DEBUG):
    #     my_function()
    # my_function()

    with log_level(logging.DEBUG, 'my-log') as logger:
        logger.debug('Debug message')
        logging.debug('Will not print')
