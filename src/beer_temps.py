#!/usr/bin/python
# -*- coding: utf-8 -*
import json
import requests
import ConfigParser
import logging
import sys
import os
import glob

logger = logging.getLogger(__name__)

class BeerTemps():
	sensor_protocol = None
	SENSOR_DS18B20 = "ds18b20"
	SENSOR_HTTP = "http"
	sensor_id = None
	sensor_url = None
	sensor_metric = False

	def __init__(self, sensor_protocol, sensor_id=None, sensor_url=None, sensor_metric = False):
		"""

		"""
		if sensor_protocol != self.SENSOR_DS18B20 and sensor_protocol != self.SENSOR_HTTP:
			logger.error("Configuration error. temperature sensor_protocol must map to DS18B20 or HTTP")
			sys.exit(1)
		self.sensor_protocol = sensor_protocol
		self.sensor_id = sensor_id
		self.sensor_url = sensor_url
		self.sensor_metric = sensor_metric

		if sensor_protocol == self.SENSOR_DS18B20:
			os.system('modprobe w1-gpio')
			os.system('modprobe w1-therm')
			if sensor_id is None: 
				self.sensor_id = self.get_ds18b20_sensor_ids()[0] # if user does not specify, just pick the first one.
		return

	def get_temperature_http(self):
		try:
			r = requests.get(self.sensor_url)
			if r.status_code == 200:
				return r.text
			else:
				logger.error("error: temperature sensor recieved http_code %i" % r.status_code)
		except:
			logger.error("Temperature. Unable to get temperature from sensor_url: %s" % self.sensor_url)

	# ds18b20 specific sensor code below
	def get_temperature(self):
		if self.sensor_protocol == self.SENSOR_HTTP:
			return self.get_temperature_http()
		else:
			return self.read_ds18b20_sensor(self.sensor_id)

	def c_to_f(self,temperature):
		return (temperature * 9.0 / 5.0 + 32.0)

	def read_ds18b20_sensor(self,sensor_id):
		lines = self.read_temp_raw(sensor_id)
		return self.process_raw_ds18b20_data(lines, sensor_id)

	def get_ds18b20_sensor_ids(self):
		base_dir = '/sys/bus/w1/devices/'
		NUM_SENSORS = len(glob.glob(base_dir + '28*'))
		sensor_ids=[]
		for x in range(0,NUM_SENSORS):
			device_folder = glob.glob(base_dir + '28*')[x]
			id = device_folder.replace("/sys/bus/w1/devices/",'')
			sensor_ids.append(id)
			logger.info("discovered sensor id %s " % str(id))
		return sensor_ids

	def process_raw_ds18b20_data(self, lines, sensor_id):
	    while lines[0].strip()[-3:] != 'YES': # TODO: wtf is this shit
	        time.sleep(0.2)
	        lines = self.read_temp_raw(sensor_id)
	    equals_pos = lines[1].find('t=')
	    if equals_pos != -1:
	        temp_string = lines[1][equals_pos+2:]
	        temp_c = float(temp_string) / 1000.0
	        if self.sensor_metric:
	        	return temp_c
	        else:
	        	return self.c_to_f(temp_c)

	def read_temp_raw(self, sensor_id):
	    base_dir = '/sys/bus/w1/devices/'
	    device_folder = glob.glob(base_dir + sensor_id)[0]
	    device_file = device_folder + '/w1_slave'
	    f = open(device_file, 'r')
	    lines = f.readlines()
	    f.close()
	    return lines



def main():
	t = BeerTemps(sensor_protocol="ds18b20")
	print "Read in: %s " % str(t.get_temperature())

if __name__ == "__main__":
	main()

