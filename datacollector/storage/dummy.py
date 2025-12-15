""" DummyStorage """
from datacollector.logger.log import LOGGER
from datacollector.storage.abstract_storage import AbstractStorage

class DummyStorage(AbstractStorage):

    """ DummyStorage """

    def _init_from_env(self):
        """ Get env variables """
        return

    def connect(self):
        return True

    def store(self, topic, key, value):
        LOGGER.info("%s:%s:%s", topic, key, value)
