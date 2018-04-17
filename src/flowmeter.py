import time
import random
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
  flow = 0 # in Liters per second
  thisPour = 0.0 # in Liters
  totalPour = 0.0 # in Liters
  tap_id = 0
  pin = -1


  def __init__(self, displayFormat, beverage, tap_id, pin):
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

  def get_pin(self):
    return self.pin

  def update(self, currentTime):
    self.clicks += 1
    # get the time delta
    self.clickDelta = max((currentTime - self.lastClick), 1)
    # calculate the instantaneous speed
    if (self.enabled == True and self.clickDelta < 1000):
      self.hertz = FlowMeter.MS_IN_A_SECOND / self.clickDelta

      # The Meat
      self.flow = self.hertz / (FlowMeter.SECONDS_IN_A_MINUTE * 7.5)  # In Liters per second
      instPour =( self.flow * (self.clickDelta / FlowMeter.MS_IN_A_SECOND)  ) #* 1.265 #1.265

      self.thisPour += instPour
      self.totalPour += instPour
    # Update the last click
    self.lastClick = currentTime

  def getBeverage(self):
    return str(random.choice(self.beverage))

  def get_tap_id(self):
    return self.tap_id

  def getFormattedThisPour(self):
    if(self.displayFormat == 'metric'):
      return str(round(self.thisPour,3)) + ' L'
    else:
      return str(round(self.thisPour * FlowMeter.PINTS_IN_A_LITER, 3)) + ' pints'
  
  def clear(self):
    self.thisPour = 0;
    self.totalPour = 0;
