import logging


def determine_weight(volume, density):
    if density <= 0:
        raise NegativeDensityError


class Error(Exception):
    """Base-class for all exceptions raised by this module"""


class WeightError(Error):
    """Base class for weight calculation errors"""


class VolumeError(Error):
    """Base class for volume calculation errors"""


class DensityError(Error):
    """Base-class for density calculation errors"""


class InvalidDensityError(Error):
    """There was a problem with a provided density value"""


class NegativeDensityError(InvalidDensityError):
    """A provided density value was negative"""

try:
    weight = determine_weight(1, -1)
except NegativeDensityError as error:
    raise ValueError('Must supply non-negative density') from error
except InvalidDensityError:
    weight = 0
except Error as error:
    logging.error('Bug in the calling code: {}'.format(error))
except Exception as error:
    logging.error('Nug in the API code: {}'.format(error))
