'''
Created on Jan 27, 2020

@author: ubuntu
'''
import argparse
import os

from datacollector.mqtt.qclient import QClient
from datacollector.logger.log import LOGGER
from datacollector.storage.storage_factory import StorageFactory

BASE_DIR=os.path.dirname(os.path.realpath(__file__))

def _init_from_env(storage):
    """ Initialize collector from environment variables """
    env_storage = os.getenv('DATACOLLECTOR_STORAGE')
    if env_storage is None:
        env_storage = storage
    return env_storage

def options():
    """Parse and polish the command-line options
    and supply reasonable defaults."""
    arg_parser = argparse.ArgumentParser(description='DataCollector', usage="%(prog)s [-s <storage to use>]")
    arg_parser.add_argument('--storage', '-s', choices=['dummy', 'mysql'], default='dummy', const='dummy', nargs='?', help='Select the storage tpe')
    opt = arg_parser.parse_args()
    return opt

def main():
    opt = options()
    storage = _init_from_env(opt.storage)
    LOGGER.info("Using Storage: {}".format(storage))
    processor = StorageFactory.get_storage(storage)
    qclient = QClient(processor)
    qclient.connect()

if __name__ == '__main__':
    main()
