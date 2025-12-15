import unittest
from unittest.mock import patch, MagicMock
from ddt import ddt, data, unpack
import paho.mqtt.client as mqtt
from datacollector.mqtt.qclient import QClient


@ddt
class InitFromEnvTests(unittest.TestCase):

    def setUp(self):
        # Use a MagickMock for the MqttClient
        self.mqtt_client = MagicMock()
        self.mqtt_client.connect.return_value = mqtt.MQTT_ERR_SUCCESS

    @data(
        ("QCLIENT_BROKER_HOST", "broker_host", "127.0.0.2"),
        ("QCLIENT_BROKER_PORT", "broker_port", "42")
    )
    @unpack
    def test_initFromEnv_ifValueIsConfiguredInEnvironemnt_setsConfiguredValueCorrectly(self, key, attribute, new_value):
        with patch('datacollector.mqtt.qclient.MqttClient') as mqtt_mock:
            # Arrange
            expected = new_value
            # - Use mock to QClient instead of real MqttClient
            mqtt_mock.return_value = self.mqtt_client

            # Act
            qclient = None
            with patch.dict("os.environ", {key: str(new_value)}):
                # - Create QClient, which invokes _init_from_env
                qclient = QClient(None)

            # Assert
            self.assertEqual(getattr(qclient, attribute), expected)
