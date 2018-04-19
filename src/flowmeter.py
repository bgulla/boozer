import time
import random
import logging
import RPi.GPIO as GPIO

"""
Flowmeter code for BOOZER

"""

log = logging.getLogger(__name__)
GPIO.setmode(GPIO.BCM)  # use real GPIO numbering


class FlowMeter():
    PINTS_IN_A_LITER = 2.11338
    SECONDS_IN_A_MINUTE = 60
    MS_IN_A_SECOND = 1000.0
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

    def __init__(self, displayFormat, beverage, tap_id, pin):
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
        self.lastClick = int(time.time() * FlowMeter.MS_IN_A_SECOND)
        self.clickDelta = 0
        self.hertz = 0.0
        self.flow = 0.0
        self.thisPour = 0.0
        self.totalPour = 0.0
        self.enabled = True
        self.tap_id = tap_id
        self.pin = pin

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

    def update(self, currentTime):
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
            self.hertz = FlowMeter.MS_IN_A_SECOND / self.clickDelta

            # The Meat
            self.flow = self.hertz / (FlowMeter.SECONDS_IN_A_MINUTE * 7.5)  # In Liters per second
            instPour = (self.flow * (self.clickDelta / FlowMeter.MS_IN_A_SECOND))  # * 1.265 #1.265

            self.thisPour += instPour
            self.totalPour += instPour
        # Update the last click
        self.lastClick = currentTime

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

    def getFormattedThisPour(self):
        """
        Returns a string representation of this current pour event.

        :return: string
        """
        if (self.displayFormat == 'metric'):
            return str(round(self.thisPour, 3)) + ' L'
        else:
            return str(round(self.thisPour * FlowMeter.PINTS_IN_A_LITER, 3)) + ' pints'

    def clear(self):
        """
        Clears an event.
        :return: nada
        """
        self.thisPour = 0;
        self.totalPour = 0;
