#!/usr/bin/python
"""
MQTT library for BOOZER.

"""
import paho.mqtt.client as paho
from random import randint
import logging
logger = logging.getLogger(__name__)


class BoozerMqtt():

    def __init__(self, brokerhost, port=1883):
        """
        Initializes the Boozer MQTT client library.

        :param brokerhost:
        :param port:
        """
        self.broker = brokerhost
        self.port = int(port)

    def pub_mqtt(self, topic, value):
        """
        Publishes a new value to a mqtt topic.

        :param topic: bar/tap{1,2,3,4}
        :param value: total remaining beer to display

        :return: nothing
        """
        client1 = paho.Client("control1")  # create client object
        try:
            client1.connect(self.broker, self.port)  # establish connection
        except:
            logger.error("unable to connect to mqtt on %s:%i" % (self.broker, self.port))
        logger.info("mqtt topic updated: topic: " + topic + " | value: " + value)
        return client1.publish(topic, value)  # publish

    def get_value(self, topic):
        """
        Returns the value of a topic from the mqtt broker.

        :param topic: bar/tap{1,2,3,4}
        :return: string representation of a float.

        """
        client1 = paho.Client("control1")  # create client object
        try:
            client1.connect(self.broker, self.port)  # establish connection
        except:
            logger.error("unable to connect to mqtt on %s:%i" % (self.broker, self.port))
        return str(client1.get(topic))
