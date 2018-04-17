#!/usr/bin/python

import paho.mqtt.client as paho
from random import randint


#def on_publish():
#  dfs

def pub_mqtt(broker,topic,value,port=1883):
  client1= paho.Client("control1")                           #create client object
  client1.connect(broker,port)                                 #establish connection
  print "[MQTT BROKER CONNECTION SUCCESSFULL] topic: %s | value: %s " % (topic,value)

  ret= client1.publish(topic,value)                   #publish


def get_value(broker,topic,port=1883):
  client1= paho.Client("control1")                           #create client object
  client1.connect(broker,port)                                 #establish connection
  val = client1.get(topic)
  return str(val)

def test_case(broker,port=1883):
  topic = "testcase/val"
  rand_val = str(randint(0, 9)) # generate temporary value
  pub_mqtt(broker,topic,rand_val)
  try:
    if get_value(broker,topic) == rand_val:
      return True
  except:
    return False
  finally:
    return False

if __name__ == '__main__':
  pub_mqtt("10.10.8.101","test/val","69.123",port=1883)
