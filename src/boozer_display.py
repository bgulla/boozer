#!/usr/bin/python
# -*- coding: utf-8 -*
import scrollphat
import logging
import time
import sys

logger = logging.getLogger(__name__)

class BoozerDisplay():

	BRIGHTNESS = 7

	def __init__(self):
		"""
		Initializes the Slack client library.

		"""
		scrollphat.set_brightness(self.BRIGHTNESS)

	def set_display(self, msg):
		scrollphat.write_string(str(msg))
		return

	def clear(self):
		scrollphat.clear()
		return

	def scroll_once(self,msg):
		scrollphat.write_string(msg, 11)
		length = scrollphat.buffer_len()

		for i in range(length):
		    try:
		        scrollphat.scroll()
		        time.sleep(0.1)
		    except KeyboardInterrupt:
		        scrollphat.clear()
		return

def main():
	lcd = BoozerDisplay()
	msg = "uBoozer"
	lcd.scroll_once(msg[1:])
	return 0



if __name__ == "__main__":
	sys.exit(main())

