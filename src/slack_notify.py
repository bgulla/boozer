#!/usr/bin/python
# -*- coding: utf-8 -*
import json
import requests
import ConfigParser
import logging

logger = logging.getLogger(__name__)

class SlackNotify():

	webhook_url = None

	def __init__(self, webhook_url):
		"""
		Initializes the Slack client library.

		"""

		if webhook_url is None:
			logger.error("SLACK - unable to init Slack obj, webhook_url was None.")
			return 

		self.webhook_url = webhook_url

	def post_slack_msg(self,msg):
		"""
		Sends a string message to slack to post.

		:param slack: string.
		:return: nada
		"""

		if self.webhook_url is None:
			logger.error("SLACK unable to post slack update, webhook_url is None")
			return

		slack_data = {'text': msg}

		response = requests.post(
			self.webhook_url, data=json.dumps(slack_data),
			headers={'Content-Type': 'application/json'}
			#self.logger.info("Slack msg sent: %s" % msg)
		)
		if response.status_code != 200:
			raise ValueError(
				'Request to slack returned an error %s, the response is:\n%s'
				% (response.status_code, response.text)
			)
			#self.logger.error("Slack unable to post msg: %s" % msg)
		return


def main():
	webhook_url = raw_input("webhook_url:")
	if webhook_url is not None and len(webhook_url) > 5:
		slack = SlackNotify(webhook_url)
		slack.post_slack_msg("Testing slack update from the main function.")
	else:
		logger.error("Unable to post to slack. webhook_url may be invalid.")
	return

if __name__ == "__main__":
	main()

