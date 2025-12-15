""" MQTT message qclient """
import os
########## Connection methods ######################
import uuid
import paho.mqtt.client as mqtt
import socket
from time import sleep, time
from datacollector.logger.log import LOGGER

class MqttClient(mqtt.Client):

    def _sock_recv(self, bufsize):
        try:
            return super()._sock_recv(bufsize)
        except AttributeError as exc:
            LOGGER.debug("Socket None workaround: %s", exc)
            raise socket.error

class QClient:
    """ MQTT message qclient """

    DEFAULT_KEEPALIVE = 30
    VALID_TRANSPORT_TYPES = ["tcp", "websockets"]

    def __init__(self, processor, topic="#"):
        """ Instantiate mqtt qclient"""

        # connection string will be read from env variables
        self.broker_host = "172.17.0.1"
        self.broker_port = "1883"
        self.broker_keepalive = QClient.DEFAULT_KEEPALIVE
        self.topic = topic
        self.transport = "tcp"

        self.processor = processor

        self.publish_calls = 0
        self.publish_callbacks = 0

        self.active = False
        self._init_from_env()
        self._init_qclient()

    def _init_qclient(self):
        """ _init_qclient """
        LOGGER.info("_init_qclient - ENTER")
        # different id for each workspace
        random_id = str(uuid.uuid4())[0:10]
        client_id = 'Producer-' + random_id
        LOGGER.info("Init mqtt client, transport = %s", self.transport)
        self.client = MqttClient(client_id=client_id, transport=self.transport)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_unsubscribe = self.on_unsubscribe
        self.client.on_message = self.on_message
        self.client.on_socket_close = self.on_socket_close

        LOGGER.info("_init_qclient - LEAVE")

    def _init_from_env(self):
        """ Initialize consumer from environment variables """
        env_broker_host = os.getenv('QCLIENT_BROKER_HOST')
        env_broker_port = os.getenv('QCLIENT_BROKER_PORT')

        if env_broker_host is not None:
            self.broker_host = str(env_broker_host)

        if env_broker_port is not None:
            self.broker_port = str(env_broker_port)

    def connect(self):
        """ This function will establish the connection to the mqtt broker
        and will not return until disconnect has been called!
        """
        self.__connect()

    def disconnect(self):
        """ Disconnect """
        if self.client is not None:
            self.client.unsubscribe(self.topic)
            LOGGER.debug("disconnect - unsubscribed")
            self.client.disconnect()
            LOGGER.debug("disconnect - disconnected")


    def __connect(self):
        """ Connect """
        LOGGER.debug("__connect - DNS entry %s port %s", self.broker_host, str(self.broker_port))
        #self.client.connect_async(self.broker_host, int(self.broker_port), self.broker_keepalive)
        self.client.connect(self.broker_host, int(self.broker_port), self.broker_keepalive)
        self.client.loop_forever(retry_first_connection=True)


########## Callbacks ###############################
    def on_connect(self, client, userdata, flags, reason_code, properties=None):
        """ Callback triggered when the listener connects to the broker. """
        LOGGER.debug(userdata)
        LOGGER.debug(flags)

        del client, userdata, flags
        LOGGER.debug("on_connect - Connected with reason code %s and properties: %s\n", str(reason_code), str(properties))

        if reason_code == 135:
            LOGGER.info("on_connect - Bad username or password.Exiting...")
            self.disconnect()
        else:
            LOGGER.debug("on_connect - Subscribing for topic: %s \n", self.topic)
            self.client.subscribe(self.topic, 1)


    def on_socket_close(self, client, sock):
        """ Callback triggered when the socket connection is closed. """
        del sock
        LOGGER.debug("on_socket_close - connection closed from qclient %s.", client._client_id)

    def on_disconnect(self, client, userdata, reason_code, properties=None):
        """ Callback triggered when a listeners disconnects. """
        del client, userdata
        LOGGER.debug("on_disconnect - Disconnected with reason code %s\n", reason_code)

        if properties:
            LOGGER.debug("on_disconnect - Disconnected with properties %s\n", str(properties))

        #self.__reconnect(False)


    def on_subscribe(self, client, userdata, mid, reason_codes, properties=None):
        """ Callback triggered when a listeners subscribes to a topic. """
        del client, userdata
        rc = reason_codes[0]
        LOGGER.debug("on_subscribe - Subscribed: %s, Reason code: %s, Properties: %s", mid, str(rc), properties)

        # if reason code is not authorized, disconnect the listener
        if rc == 135:
            # means we are not authorized to subscribe to this topic
            LOGGER.info("User is not authorized to subscribe to topic %s. Disconnecting...", self.topic)
            self.disconnect()

        else:
            self.active = True

    def on_unsubscribe(self, client, userdata, mid):
        """ Callback triggered when a listeners unsubscribes from a topic. """
        del client, userdata
        LOGGER.debug("on_unsubscribe - Unsubscribed: %s \n", mid)

    def on_message(self, client, userdata, message):
        """ Callback triggered when a message is received. """
        del client, userdata
        LOGGER.debug("on_message - Received: %s  /// %s \n", message.topic, message.payload)
        self.processor.process(message.topic, message.payload)


########## Getters and setters #####################
    def get_topic(self):
        """ Getter """
        return self.topic

    def set_topic(self, value):
        """ Setter """
        self.topic = str(value)

    def is_active(self):
        """ Getter """
        return self.active

    def get_number_publish_calls(self):
        return self.publish_calls

    def get_number_publish_callbacks(self):
        return self.publish_callbacks
