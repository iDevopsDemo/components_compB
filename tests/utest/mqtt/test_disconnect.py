import unittest
from unittest.mock import patch, MagicMock
import paho.mqtt.client as mqtt
from datacollector.mqtt.qclient import QClient


class DisconnectTests(unittest.TestCase):

    def setUp(self):
        # Use a MagickMock for the MqttClient
        self.mqtt_client = MagicMock()
        self.mqtt_client.connect.return_value = mqtt.MQTT_ERR_SUCCESS

    @patch('datacollector.mqtt.qclient.MqttClient')
    def test_disconnect_withMqttClient_wantsToDisconnectFromServer(self, mqtt_mock):
        # Arange
        expected_port = 1883
        # - Use mock to QClient instead of real MqttClient
        mqtt_mock.return_value = self.mqtt_client
        # - Create QClient, which invokes connect
        qclient = QClient(None)
        qclient.connect()

        # Act
        qclient.disconnect()

        # Assert
        self.mqtt_client.disconnect.assert_called()
        self.assertFalse(qclient.is_active())
