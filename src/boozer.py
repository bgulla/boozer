#!/usr/bin/python
# -*- coding: utf-8 -*

import os
import time
import math
import logging
#import scrollphat
# import RPi.GPIO as GPIO
from flowmeter import *
import beer_db
import twitter_notify
import slack_notify
import requests
import ConfigParser
import logging
import bar_mqtt

####

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
import time


####



scrollphat_cleared = True

# Setup the configuration
CONFIG_FILE = "./config.ini"
config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE)

db = beer_db.BeerDB("./db.sqlite")  # TODO: replace this with configuration value

MQTT_ENABLED = False
TWITTER_ENABLED = False
SCROLLPHAT_ENABLED = False
SLACK_ENABLED = False
TEMPERATURE_ENABLED = False

#if config.get("Scrollphat", 'enabled') == "True":
#    scrollphat.set_brightness(7)

# Set the logger
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)


import os 
current_path = os.path.dirname(os.path.realpath(__file__))

# setup twitter client
if config.getboolean("Twitter", "enabled"):
    TWITTER_ENABLED = True
    twitter = twitter_notify.TwitterNotify(config)

# setup mqtt client
if config.getboolean("Mqtt", "enabled"):
    MQTT_ENABLED = True
    mqtt_client = bar_mqtt.BoozerMqtt(config.get("Mqtt", "broker"))

# setup temperaturesensor client
if config.getboolean("Temperature", "enabled"):
    TEMPERATURE_ENABLED = True
    temperature_url = config.get("Temperature", "endpoint")



# setup slack client
if config.getboolean("Slack", "enabled"):
    SLACK_ENABLED = True
    slack = slack_notify.SlackNotify(config)

# set up the flow meters
taps = []  # TODO, make this dynamic by reading teh configuration files
# Tap 1
tap1 = FlowMeter("not metric", [config.get("Taps", "tap1_beer_name")], tap_id=1,
                 pin=config.getint("Taps", "tap1_gpio_pin"))
tap2 = FlowMeter("not metric", [config.get("Taps", "tap2_beer_name")], tap_id=2,
                 pin=config.getint("Taps", "tap2_gpio_pin"))
tap3 = FlowMeter("not metric", [config.get("Taps", "tap3_beer_name")], tap_id=3,
                 pin=config.getint("Taps", "tap3_gpio_pin"))
tap4 = FlowMeter("not metric", [config.get("Taps", "tap4_beer_name")], tap_id=4,
                 pin=config.getint("Taps", "tap4_gpio_pin"))
taps = {tap1, tap2, tap3, tap4}

# More config

def get_enabled_string(val):
    if val == True:
        return "enabled"
    else:
        return "disabled"

def print_config(config):  ## WHY AM I PRINTING? TODO switch to log.info()
    print "BOOZER IS UP. LET'S FUCKING DO THIS"
    print "==================================="
    print "Twitter: ", get_enabled_string(TWITTER_ENABLED)
    print "MQTT: ", get_enabled_string(MQTT_ENABLED)
    print "Temperature: ", get_enabled_string(TEMPERATURE_ENABLED)
    print "Slack: ", get_enabled_string(SLACK_ENABLED)
    print "==================================="


def get_temperature():
    """
    Parses a http GET request for the connected temperature sensor. Yes, this
    relies on an external sensor-serving process, I recommend https://github.com/bgulla/sensor2json

    :return: string
    """
    global TEMPERATURE_ENABLED
    if not TEMPERATURE_ENABLED:
      return "disabled"
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
    db.update_tap(tap_id, pour)


def update_mqtt(tap_id):
    """

    :param tap_id:
    :return:
    """
    percent = db.get_percentage100(tap_id)
    topic = "bar/tap%s" % str(tap_id)
    mqtt_client.pub_mqtt(topic, str(percent))

def scroll_once(msg):
    serial = i2c(port=1, address=0x3C)
    device = ssd1306(serial, rotate=0)
    with canvas(device) as draw:
#    draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((40, 40), msg, fill="white")
        if True:
            time.sleep(0.1)

def display(msg):
    if SCROLLPHAT_ENABLED:
        scroll_once(msg)
    else:
        display_lcd(msg)

def scroll_once2(msg):
    scrollphat.write_string(msg, 11)
    length = scrollphat.buffer_len()

    for i in range(length):
        try:
            scrollphat.scroll()
            time.sleep(0.1)
        except KeyboardInterrupt:
            scrollphat.clear()

def register_tap(tap_obj):
    """

    :param tap_obj:
    :return:
    """
    currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
    tap_obj.update(currentTime)
    logger.info("event-bus: registered tap " + str(tap_obj.get_tap_id()) + "successfully")


for tap in taps:  # setup all the taps. add event triggers to the opening of the taps.
    GPIO.add_event_detect(tap.get_pin(), GPIO.RISING, callback=lambda *a: register_tap(tap), bouncetime=20)
    if MQTT_ENABLED: update_mqtt(tap.get_tap_id()) # do a prelim mqtt update in case it's been awhile

# Initial info
if TEMPERATURE_ENABLED:
    logger.info("Temperature: " + get_temperature())


print_config(config)
logger.info("Boozer Intialized! Waiting for pours. Drink up, be merry!")

while True:

    # Handle keyboard events
    currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)

    for tap in taps:
        if tap.thisPour > 0.0:
            pour_size = round(tap.thisPour * FlowMeter.PINTS_IN_A_LITER, 3)
            pour_size2 = round(tap.thisPour * FlowMeter.PINTS_IN_A_LITER,
                               2)  # IDK what is going on here but it works and I am afraid to break it
            if pour_size != tap.previous_pour:
                logger.debug(
                    "Tap: %s\t Poursize: %s vs %s" % (str(tap.get_tap_id()), str(pour_size), str(tap.previous_pour)))
#                scrollphat.set_brightness(7)
                if pour_size2 < 0.05:
                    continue
                scroll_once(str(pour_size2).replace("0.", "."))

#                scrollphat.write_string(str(pour_size2).replace("0.", "."))
                tap.set_previous_pour(pour_size)
                scrollphat_cleared = False

        if (tap.thisPour > 0.23 and currentTime - tap.lastClick > 10000):  # 10 seconds of inactivity causes a tweet

            pour_size = round(tap.thisPour * FlowMeter.PINTS_IN_A_LITER, 3)
            # receord that pour into the database
            db.update_tap(tap.tap_id, pour_size) # record the pour in the db

            # is twitter enabled?
            if TWITTER_ENABLED:
                # calculate how much beer is left in the keg
                volume_remaining = str(round(db.get_percentage(tap.get_tap_id()), 3) * 100)
                # tweet of the record
                msg = twitter.tweet_pour(tap.get_tap_id(),
                                   tap.getFormattedThisPour(),
                                   tap.getBeverage(),
                                   volume_remaining,
                                   get_temperature())  # TODO make temperature optional
                if SCROLLPHAT_ENABLED : scroll_once(msg)


            if SLACK_ENABLED:
                # calculate how much beer is left in the keg
                volume_remaining = str(round(db.get_percentage(tap.get_tap_id()), 3) * 100)
                # tweet of the record
                msg = slack.slack_pour(tap.get_tap_id(),
                                   tap.getFormattedThisPour(),
                                   tap.getBeverage(),
                                   volume_remaining,
                                   get_temperature())  # TODO make temperature optional

            # reset the counter
            tap.thisPour = 0.0

            # clear the display
#            scrollphat.clear()
#            scrollphat_cleared = True

            # publish the updated value to mqtt broker
            if config.getboolean("Mqtt", "enabled"): update_mqtt(tap.get_tap_id())

        # display the pour in real time for debugging
        if tap.thisPour > 0.05: logger.debug("[POUR EVENT] " + str(tap.get_tap_id()) + ":" + str(tap.thisPour))

        # reset flow meter after each pour (2 secs of inactivity)
        if (tap.thisPour <= 0.23 and currentTime - tap.lastClick > 2000): tap.thisPour = 0.0

    # go night night
    time.sleep(0.01)
