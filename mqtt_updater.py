#!/usr/bin/python

import beer_database as db
import ConfigParser
import paho.mqtt.client as paho
from random import randint
import bar_mqtt

CONFIG_FILE="/opt/beer-meter/config.ini"
config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE)

def get_value(broker,topic,port=1883):
  client1= paho.Client("control1")                           #create client object
  client1.connect(broker,port)                                 #establish connection
  val = client1.get(topic)
  return str(val)

def update_mqtt(tap_id):
  global config
  broker = config.get("Mqtt","broker")
  percent= db.get_percentage100(tap_id)
  topic = "bar/tap%s" % str(tap_id)
  bar_mqtt.pub_mqtt(broker,topic,str(percent))
  

if __name__ == '__main__':
  update_mqtt(1) 
  update_mqtt(2) 
  update_mqtt(3) 
  update_mqtt(4) 


