import time
import random
import logging
import RPi.GPIO as GPIO


### Begin. These probably need to be pulled.
import beer_db
import twitter_notify
import slack_notify
import requests
import ConfigParser
import logging
import zope.event
### End


# Event vars
POUR_RESET = 1
POUR_FULL = 3
POUR_UPDATE = 5


"""
Flowmeter code for BOOZER

"""

logger = logging.getLogger(__name__)
GPIO.setmode(GPIO.BCM)  # use real GPIO numbering


class FlowMeter():
    PINTS_IN_A_LITER = 2.11338
    SECONDS_IN_A_MINUTE = 60
    MS_IN_A_SECOND = 1000.0
    POUR_THRESHOLD = 0.23 ## This is the minimum amount of volume to be poured before it is registered as a complete pour.
    displayFormat = 'metric'
    beverage = 'beer'
    enabled = True
    clicks = 0
    lastClick = 0
    clickDelta = 0
    hertz = 0.0
    flow = 0  # in Liters per second
    thisPour = 0.0  # in Liters
    totalPour = 0.0  # in Liters
    tap_id = 0
    pin = -1
    previous_pour = 0.0
    STANDALONE_MODE = False
    config = False
    last_event_type = POUR_RESET # this baselines the pour event to be reset

    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.INFO)

    def __init__(self, displayFormat, beverage, tap_id, pin, config, STANDALONE_MODE=False):
        """
        Initializes the FlowMeter object.

        :param displayFormat: metric or not?
        :param beverage: name of the beverage passing through the line
        :param tap_id: how shall i identify myself?
        :param pin: the GPIO pin to listen on
        """
        self.displayFormat = displayFormat
        self.beverage = beverage
        self.clicks = 0
        self.lastClick = int(time.time() * self.MS_IN_A_SECOND)
        self.clickDelta = 0
        self.hertz = 0.0
        self.flow = 0.0
        self.thisPour = 0.0
        self.totalPour = 0.0
        self.enabled = True
        self.tap_id = tap_id
        self.pin = pin
        self.config = config # TODO: find a way to pull this out and make it decoupled from the config object
        self.STANDALONE_MODE = STANDALONE_MODE

        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def get_pin(self):
        """
        Return the GPIO pin that the flowmeter is connected to.

        :return: int
        """
        return self.pin

    def set_previous_pour(self, vol):
        """
        Updates the last pour event's volume.

        :param vol: float
        :return:
        """
        self.previous_pour = vol

    def update(self, currentTime=int(time.time() * MS_IN_A_SECOND)):
        """
        Sets a timestamp of the last pour event.

        :param currentTime: timestamp of a long
        :return: nada
        """
        self.clicks += 1
        # get the time delta
        self.clickDelta = max((currentTime - self.lastClick), 1)
        # calculate the instantaneous speed
        if (self.enabled == True and self.clickDelta < 1000):
            self.hertz = self.MS_IN_A_SECOND / self.clickDelta

            # The Meat
            self.flow = self.hertz / (self.SECONDS_IN_A_MINUTE * 7.5)  # In Liters per second
            instPour = (self.flow * (self.clickDelta / self.MS_IN_A_SECOND))  # * 1.265 #1.265

            self.thisPour += instPour
            self.totalPour += instPour
        # Update the last click
        self.lastClick = currentTime

        # Log it
#        self.logger.info("event-bus: registered tap " + str(self.get_tap_id()) + " successfully")
        self.logger.info("Tap[%i] reading: %s" %( self.get_tap_id(), str(self.totalPour)))

    def getBeverage(self):
        """
        Returns the name of the beverage being served.

        :return: string
        """
        # return str(random.choice(self.beverage))
        return self.beverage

    def get_tap_id(self):
        """
        Returns the tap identifier as an int.
        :return: int
        """
        return self.tap_id
    
    def reset_pour_status(self):
        """
        This will reset a pour to a cleared event. this is needed to properly track what beer has already been registered in the database.
        """
        self.last_event_type = POUR_RESET

    def getFormattedThisPour(self):
        """
        Returns a string representation of this current pour event.

        :return: string
        """
        if (self.displayFormat == 'metric'):
            return str(round(self.thisPour, 3)) + ' L'
        else:
            return str(round(self.thisPour * self.PINTS_IN_A_LITER, 3)) + ' pints'

    def clear(self):
        """
        Clears an event.
        :return: nada
        """
        self.thisPour = 0
        self.totalPour = 0

    def listen_for_pour(self):
        """
        """
        currentTime = int(time.time() * self.MS_IN_A_SECOND)
        
        if self.thisPour > 0.0:
            pour_size = round(self.thisPour * self.PINTS_IN_A_LITER, 3)
            pour_size2 = round(self.thisPour * self.PINTS_IN_A_LITER,2)  # IDK what is going on here but it works and I am afraid to break it
            if pour_size != self.previous_pour:
                self.logger.debug(
                    "Tap: %s\t Poursize: %s vs %s" % (str(self.tap_id), str(pour_size), str(self.previous_pour)))
                if pour_size2 < 0.05:
                    return # ignore small events
                self.set_previous_pour(pour_size)
                self.last_event_type = POUR_UPDATE # set last event status for event bus in boozer

        ## Test if the pour is above the minimum threshold and if so, register and complete the pour action.
        if (self.thisPour > self.POUR_THRESHOLD and currentTime - self.lastClick > 10000):  # 10 seconds of inactivity causes a tweet
            self.register_new_pour(currentTime)
            self.last_event_type = POUR_FULL # set last event status for event bus in boozer
        
        zope.event.notify(self) # notify the boozer event bus that a new pour has been registered. 
                                # it will check 'last_event_type' to decide to kick off actions related to a full pour up just update the database for a half/min pour.

    def register_new_pour(self, currentTime):
        """
        """
        pour_size = round(self.thisPour * self.PINTS_IN_A_LITER, 3)
                # record that pour into the database
        # reset the counter
        self.thisPour = 0.0

        # display the pour in real time for debugging
        if self.thisPour > 0.05: self.logger.debug("[POUR EVENT] " + str(self.tap_id) + ":" + str(self.thisPour))

        # reset flow meter after each pour (2 secs of inactivity)
        if (self.thisPour <= self.POUR_THRESHOLD and currentTime - self.lastClick > 2000): self.thisPour = 0.0


def main():

    # bring in config
    CONFIG_FILE = "./config.ini"
    config = ConfigParser.ConfigParser()
    config.read(CONFIG_FILE)
    # setup logging
    # do it
    test_tap_id = 4
    test_tap_gpio_pin = 13
    test_tap = FlowMeter("not metric", "FlowmeterTestBeer", tap_id=4, pin=test_tap_gpio_pin, config=config, STANDALONE_MODE=True)

    # setup the flowmeter event bus
    GPIO.add_event_detect(test_tap.get_pin(), GPIO.RISING, callback=lambda *a: test_tap.update(), bouncetime=20)
    while True:
        test_tap.listen_for_pour()
        time.sleep(0.01)

# it's go time.
if __name__ == "__main__":
    main()
