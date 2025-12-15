import unittest
from unittest.mock import ANY, patch, MagicMock
import paho.mqtt.client as mqtt
from datacollector.mqtt.qclient import QClient


class PropertyTests(unittest.TestCase):

    def setUp(self):
        # Use a MagickMock for the MqttClient
        self.mqtt_client = MagicMock()
        self.mqtt_client.connect.return_value = mqtt.MQTT_ERR_SUCCESS

    @patch('datacollector.mqtt.qclient.MqttClient')
    def test_set_topic_is_get_topic(self, mqtt_mock):
        # Arrange
        expected_topic = "my_magic_topic"
        # - Use mock to QClient instead of real MqttClient
        mqtt_mock.return_value = self.mqtt_client
        # - Create QClient, which invokes connect
        qclient = QClient(None)
        qclient.set_topic(expected_topic)

        # Act
        # - Create QClient, which invokes connect
        actual_topic = qclient.get_topic()

        # Assert
        self.assertEqual(actual_topic, expected_topic)
