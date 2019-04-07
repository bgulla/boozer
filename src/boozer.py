#!/usr/bin/python
# -*- coding: utf-8 -*

import os
import pyfiglet 
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
import time
import zope.event
from prettytable import PrettyTable
import os 

CONFIG_FILEPATH = "./config.ini"
DB_FILEPATH = "./db.sqlite"

scrollphat_cleared = True ## TODO: decouple this

# Setup the configuration
config = ConfigParser.ConfigParser()
config.read(CONFIG_FILEPATH)

db = beer_db.BeerDB(DB_FILEPATH)  # TODO: replace this with configuration value

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


current_path = os.path.dirname(os.path.realpath(__file__))
if not os.path.isfile(DB_FILEPATH):
	logger.fatal("[fatal] cannot load db from " % DB_FILEPATH)
	sys.exit(1)
if not os.path.isfile(CONFIG_FILEPATH):
	logger.fatal("[fatal] cannot load config from " % CONFIG_FILEPATH)
	sys.exit(1)

# setup twitter client
try:
	if config.getboolean("Twitter", "enabled"):
	    TWITTER_ENABLED = True
	    twitter = twitter_notify.TwitterNotify(config)
except: 
	logger.info("Twitter Entry not found in %s, setting TWITTER_ENABLED to False")
	TWITTER_ENABLED = False

# setup mqtt client
try:
	if config.getboolean("Mqtt", "enabled"):
	    MQTT_ENABLED = True
	    mqtt_client = bar_mqtt.BoozerMqtt(config.get("Mqtt", "broker"))
except: 
	logger.info("MQTT Entry not found in %s, setting MQTT_ENABLED to False")
	MQTT_ENABLED = False

# setup temperaturesensor client
try:
	if config.getboolean("Temperature", "enabled"):
		TEMPERATURE_ENABLED = True
    	temperature_url = config.get("Temperature", "endpoint")
except: 
	logger.info("Temperature Entry not found in %s, setting TEMPERATURE_ENABLED to False")
	TEMPERATURE_ENABLED = False

# setup slack client
try:
	if config.getboolean("Slack", "enabled"):
	    SLACK_ENABLED = True
	    slack = slack_notify.SlackNotify(config)
except: 
	logger.info("Slack Entry not found in %s, setting SLACK_ENABLED to False")
	TEMPERATURE_ENABLED = False

# set up the flow meters
taps = []  
for tap in range(1,10): # limit of 10 taps
	str_tap = "tap%i" % tap 
	str_tapN_gpio_pin = "%s_gpio_pin" % str_tap
	str_tapN_beer_name = "%s_beer_name" % str_tap

	try:
		this_tap_gpio_pin = config.getint("Taps", str_tapN_gpio_pin) # this looks for the tap gpio pin such as "tap1_gpio_pin"
		this_tap_beer_name = [config.get("Taps", str_tapN_beer_name)]
		new_tap = FlowMeter("not metric", this_tap_beer_name, tap_id=tap, pin=this_tap_gpio_pin, config=config) # Create the tap object
		taps.append(new_tap) # Add the new tap object to the array
	except:
		break

if len(taps) < 1:
	# if there were no taps read in, there's no point living anymore. go fatal
	logger.fatal("FATAL - No taps were read in from the config file. Are they formatted correctly?")

# More config

def get_enabled_string(val):
    if val == True:
        return "enabled"
    else:
        return "disabled"

def print_config():
	result = pyfiglet.figlet_format("BOOZER") #, font = "slant" ) 
        print
        print
	print result

	files_table = PrettyTable(['File','Filepath', 'Exists'])
	files_table.add_row(['Database', DB_FILEPATH, os.path.isfile(DB_FILEPATH)])
	files_table.add_row(['Configuration', CONFIG_FILEPATH, os.path.isfile(CONFIG_FILEPATH)])
	print files_table

	t = PrettyTable(['Feature','Status'])
	t.add_row(['Twitter', get_enabled_string(TWITTER_ENABLED)])
	t.add_row(['Mqtt', get_enabled_string(MQTT_ENABLED)])
	t.add_row(['Temperature', get_enabled_string(TEMPERATURE_ENABLED)])
	t.add_row(['Slack', get_enabled_string(SLACK_ENABLED)])
	print t

	taps_table = PrettyTable(['Tap','Beer','GPIO Pin', 'Volume Remaining'])
	for tap in taps:
		taps_table.add_row([str(tap.get_tap_id()), str(tap.get_beverage_name()[0]), str(tap.get_pin()), str(db.get_percentage100(tap.get_tap_id()))])
	print taps_table


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


def update_display(msg):
    if SCROLLPHAT_ENABLED:
        update_scrollphat(msg)
        
def update_scrollphat(msg):
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


## TODO This needs to be pulled into the init script 
for tap in taps:  # setup all the taps. add event triggers to the opening of the taps.
    GPIO.add_event_detect(tap.get_pin(), GPIO.RISING, callback=lambda *a: register_tap(tap), bouncetime=20)
    #if MQTT_ENABLED: update_mqtt(tap.get_tap_id()) # do a prelim mqtt update in case it's been awhile

# Initial info
if TEMPERATURE_ENABLED:
    logger.info("Temperature: " + get_temperature())


def register_pour_event( tap_obj ):
    tap_event_type = tap_obj.last_event_type

    if tap_event_type == FlowMeter.POUR_FULL:
        # we have detected that a full beer was poured
        register_new_pour(tap_obj)
    elif tap_event_type == FlowMeter.POUR_UPDATE:
        # it was just a mid pour 
        # TODO: Update scrollphat here
        logger.debug("flowmeter.POUR_UPDATE")
        #print "brandon do something like update the scrollphat display or do nothing. it's cool"

zope.event.subscribers.append(register_pour_event) # Attach the event

def register_new_pour(tap_obj):
    """
    """
    
    pour_size = round(tap_obj.thisPour * tap_obj.PINTS_IN_A_LITER, 3)
            # receord that pour into the database
    
    try:
        db.update_tap(tap_obj.tap_id, pour_size) # record the pour in the db
        self.logger.info("Database updated: %s %s " % (str(tap_obj.tap_id), str(pour_size)))
    except :
        self.logger.error("unable to register new pour event to db")
	
	
	# calculate how much beer is left in the keg
	#volume_remaining = str(round(db.get_percentage(tap_obj.tap_id), 3) * 100)
	volume_remaining = str(db.get_percentage(tap_obj.tap_id))

    # is twitter enabled?
    if TWITTER_ENABLED:
    	logger.info("Twitter is enabled. Preparing to send tweet.")
        # calculate how much beer is left in the keg
        # tweet of the record
        msg = twitter.tweet_pour(tap_obj.tap_id,
                            tap_obj.getFormattedThisPour(),
                            tap_obj.getBeverage(),
                            volume_remaining,
                            get_temperature())  # TODO make temperature optional
        logger.info("Tweet Sent: %s" % msg)
        #if SCROLLPHAT_ENABLED : scroll_once(msg)

    if SLACK_ENABLED:
    	logger.info("Slack notifications are enabled. Preparing to send slack update.")
        
        # tweet of the record
        msg = slack.slack_pour(tap_obj.tap_id,
                            tap_obj.getFormattedThisPour(),
                            tap_obj.getBeverage(),
                            volume_remaining,
                            get_temperature())  # TODO make temperature optional
        logger.info("Sent slack update: %s" % msg)
    # reset the counter
    tap_obj.thisPour = 0.0
    logger.info("reseting pour amount to 0.0")

    # publish the updated value to mqtt broker
    if config.getboolean("Mqtt", "enabled"): update_mqtt(tap_obj.tap_id)

    # display the pour in real time for debugging
    if tap_obj.thisPour > 0.05: self.logger.debug("[POUR EVENT] " + str(tap_obj.tap_id) + ":" + str(tap_obj.thisPour))

def main():
    print_config()
    logger.info("Boozer Intialized! Waiting for pours. Drink up, be merry!")
    while True:

        # Handle keyboard events
        currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
        
        for tap in taps:
            tap.listen_for_pour()

        # go night night
        time.sleep(0.01)

if __name__ == "__main__":
    main()
