"""Abstract Storage Class"""

import json
from abc import ABCMeta, abstractmethod
from datacollector.logger.log import LOGGER

UNICODE_DOT = '\\u002e'
UNICODE_DOLLAR = '\\u0024'

class AbstractStorage:
    """Abstract class for Storages

    """
    __metaclass__ = ABCMeta

    def __init__(self):
        self._init_from_env()
        self.connect()

    @abstractmethod
    def _init_from_env(self):
        """This function allows to read env variables
        """

    @abstractmethod
    def connect(self):
        """This function allows to read env variables
        """

    @abstractmethod
    def store(self, topic, key, value):
        """The function receives a message from a topic and processes it
           Return status code so the calling method knows what to do next
           The method should be public.
        """

    def process(self, topic, message):
        """ Process the message received"""
        try:
            topic, key = self._convert_topic(topic)
            value = self._convert_msg(message)
            LOGGER.debug("process - persisting message")
            self.store(topic, key, value)
        except Exception as gen_exc:
            LOGGER.debug("process - Exception while processing message: %s", str(gen_exc))

    def _convert_topic(self, topic):
        LOGGER.debug("_convert_topic - ENTER converting topic; topic type: %s", type(topic))
        # convert the message to UTF-8
        if isinstance(topic, bytes):
            topic = topic.decode("utf-8")

        # if input is string
        if isinstance(topic, str):
            #first get the key
            if '/' in topic:
                index = topic.rfind('/')
                key = topic[index+1:]
                topic = topic[:topic.rfind('/')]
            else:
                key = topic
            # replace single quote with double quote
            topic = topic.replace('\'', '\"')
            # transform into Kafka SQL valid format
            # - not supported by sql
            topic = topic.replace('-', '_')
            # / not supported by both
            topic = topic.replace('/', '_')

        LOGGER.debug("_convert_topic - LEAVE")
        return topic, key

    def _convert_msg(self, message):
        LOGGER.debug("_convert_msg - ENTER converting message; message type: %s", type(message))
        # convert the message to UTF-8
        if isinstance(message, bytes):
            message = message.decode("utf-8")

        # if input is string
        if isinstance(message, str):
            # replace single quote with double quote
            message = message.replace('\'', '\"')
            # transform string to json
            LOGGER.debug("process - converting message into json format")
            message = json.loads(message)
            LOGGER.debug("_convert_msg - replacing unwanted characters; message type: %s", type(message))
            message = self._replace(message)

        LOGGER.debug("_convert_msg - LEAVE")
        return message

    def _replace(self, message):
        # iterate over keys, replace $ and . with unicode equivalent
        if isinstance(message, dict):
            return self.__replace_dict(message)
        elif isinstance(message, list):
            return self.__replace_list(message)
        else:
            return self.__replace_str(message)

    def __replace_dict(self, message):
        new_message = {}
        for k, v in message.items():
            new_key = k.replace('.', UNICODE_DOT).replace('$', UNICODE_DOLLAR)
            new_message[new_key] = self._replace(v)
        return new_message

    def __replace_list(self, message):
        new_message = []
        for item in message:
            new_message.append(self._replace(item))
        return new_message

    def __replace_str(self, message):
        # if message represents a numeric value, don't replace
        if not str(message).replace('.', '', 1).lstrip('-').isdigit():
            new_message = str(message).replace('.', UNICODE_DOT).replace('$', UNICODE_DOLLAR)
            return new_message
        return message
