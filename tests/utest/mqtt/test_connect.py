import unittest
from unittest.mock import ANY, patch, MagicMock
import paho.mqtt.client as mqtt
from datacollector.mqtt.qclient import QClient


class ConnectTests(unittest.TestCase):

    def setUp(self):
        # Use a MagickMock for the MqttClient
        self.mqtt_client = MagicMock()
        self.mqtt_client.connect.return_value = mqtt.MQTT_ERR_SUCCESS

    @patch('datacollector.mqtt.qclient.MqttClient')
    def test_connect_whenCalledWithoutEnvironment_makesMqttClientConnect_withDefaultServiceHost(self, mqtt_mock):
        # Arrange
        expected_host = "172.17.0.1"
        # - Use mock to QClient instead of real MqttClient
        mqtt_mock.return_value = self.mqtt_client

        # Act
        qclient = QClient(None)
        qclient.connect()

        # Assert
        self.mqtt_client.connect.assert_called_with(expected_host, ANY, ANY)

    @patch('datacollector.mqtt.qclient.MqttClient')
    def test_connect_whenCalledWithoutEnvironment_makesMqttClientConnect_withDefaultServicePort(self, mqtt_mock):
        # Arange
        expected_port = 1883
        # - Use mock to QClient instead of real MqttClient
        mqtt_mock.return_value = self.mqtt_client

        # Act
        qclient = QClient(None)
        qclient.connect()

        # Assert
        self.mqtt_client.connect.assert_called_with(ANY, expected_port, ANY)
