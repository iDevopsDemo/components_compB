""" Usefull class for logging."""
import logging.config
import os
from os.path import join

BASEDIR = os.path.abspath(os.path.dirname(__file__))
CONFIG_FILE_PATH = join(BASEDIR, 'log.conf')

logging.config.fileConfig(CONFIG_FILE_PATH, disable_existing_loggers=False)

# Get the logger specified in the file
LOGGER = logging.getLogger(__name__)


def disable_logging():
    """ disable_logging - useful for tests """
    logging.disable(logging.CRITICAL)
