#!/usr/bin/python
# -*- coding: utf-8 -*

import os
import time
import math
import logging
import scrollphat
#import RPi.GPIO as GPIO
from flowmeter import *
import beer_db
import twitter_notify
import requests
import ConfigParser
import logging
import bar_mqtt


GPIO.setmode(GPIO.BCM) # use real GPIO numbering

scrollphat_cleared = True


# Setup the configuration
CONFIG_FILE="./config.ini"
config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE)

db = beer_db.BeerDB("./db.sqlite") #TODO: replace this with configuration value

SCROLLPHAT_ENABLED = False
if config.get("Scrollphat",'enabled') == "True":
  scrollphat.set_brightness(7)

MQTT_ENABLED = False


# Set the logger
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


# setup twitter client
if config.getboolean("Twitter","enabled"):
  twitter = twitter_notify.TwitterNotify(config)

if config.getboolean("Mqtt","enabled"):
  MQTT_ENABLED = True
  mqtt_client = bar_mqtt.BoozerMqtt(config.get("Mqtt","broker"))


# set up the flow meters
taps = [] # TODO, make this dynamic by reading teh configuration files
# Tap 1
tap1 = FlowMeter( "not metric", [config.get("Taps", "tap1_beer_name")], tap_id=1, pin=config.getint("Taps", "tap1_gpio_pin"))
tap2 = FlowMeter( "not metric", [config.get("Taps", "tap2_beer_name")], tap_id=2, pin=config.getint("Taps", "tap2_gpio_pin"))
tap3 = FlowMeter( "not metric", [config.get("Taps", "tap3_beer_name")], tap_id=3, pin=config.getint("Taps", "tap3_gpio_pin"))
tap4 = FlowMeter( "not metric", [config.get("Taps", "tap4_beer_name")], tap_id=4, pin=config.getint("Taps", "tap4_gpio_pin"))
taps = {tap1,tap2,tap3,tap4}

# More config
temperature_url = config.get("Temperature","endpoint")

def get_temperature():
  global temperature_url
  try:
    r = requests.get(temperature_url)
    if r.status_code == 200:
      return r.text
    else:
      return "error_http"
  except:
    return "error"

def record_pour(tap_id, pour):
  db.update_tap(tap_id,pour)


def update_mqtt(tap_id):
  percent= db.get_percentage100(tap_id)
  topic = "bar/tap%s" % str(tap_id)
  mqtt_client.pub_mqtt(topic,str(percent))

# new hotness
def register_tap( tap_obj):
  currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
  tap_obj.update(currentTime)
  logger.info("event-bus: registered tap " + str(tap_obj.get_tap_id()) + "successfully" )

for tap in taps: # if something is broken, it's probably this
  GPIO.add_event_detect(tap.get_pin(), GPIO.RISING, callback=lambda *a: register_tap(tap), bouncetime=20)
  if MQTT_ENABLED : update_mqtt(tap.get_tap_id())


# Initial info
logger.info( "Temperature: " + get_temperature())
logger.info("Boozer Intialized! Waiting for pours. Drink up, be merry!")

while True:

  # Handle keyboard events
  currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)

  for tap in taps:
    if tap.thisPour > 0.0:
      pour_size = round(tap.thisPour * FlowMeter.PINTS_IN_A_LITER, 3)
      pour_size2 = round(tap.thisPour * FlowMeter.PINTS_IN_A_LITER, 2) # IDK what is going on here but it works and I am afraid to break it
      if pour_size != tap.previous_pour:
        logger.debug( "Tap: %s\t Poursize: %s vs %s" % (str(tap.get_tap_id()),  str(pour_size), str(tap.previous_pour)))
        scrollphat.set_brightness(7)
        scrollphat.write_string(str(pour_size2).replace("0.","."))
        tap.set_previous_pour(pour_size)
        scrollphat_cleared = False

    if (tap.thisPour > 0.23 and currentTime - tap.lastClick > 10000): # 10 seconds of inactivity causes a tweet

      pour_size = round(tap.thisPour * FlowMeter.PINTS_IN_A_LITER, 3)
      # receord that pour into the database
      record_pour(tap.get_tap_id(), pour_size)

      # is twitter enabled?
      if config.getboolean("Twitter", "enabled"):
        # calculate how much beer is left in the keg
        volume_remaining = str(round(db.get_percentage(tap.get_tap_id()), 3) * 100)
        # tweet of the record
        twitter.tweet_pour(tap.get_tap_id(),
                           tap.getFormattedThisPour(),
                           tap.getBeverage(),
                           volume_remaining,
                           get_temperature())

      # reset the counter
      tap.thisPour = 0.0

      # clear the display
      scrollphat.clear()
      scrollphat_cleared = True

      # publish the updated value to mqtt broker
      if config.getboolean("Mqtt","enabled"): update_mqtt(tap.get_tap_id())

    # display the pour in real time for debugging
    if tap.thisPour > 0.05: logger.debug("[POUR EVENT] " + str(tap.get_tap_id()) + ":" + str(tap.thisPour) )
    
    # reset flow meter after each pour (2 secs of inactivity)
    if (tap.thisPour <= 0.23 and currentTime - tap.lastClick > 2000): tap.thisPour = 0.0

  # go night night
  time.sleep(0.01)

