#!/usr/bin/python
# -*- coding: utf-8 -*
import json
import requests
import ConfigParser
import logging

# Static vars
DEGREES="°"

logger = logging.getLogger(__name__)

class SlackNotify():

    def __init__(self, config_obj):
        """
        Initializes the Slack client library.

        :param config_obj: SimpleConfig object used to pull the auth creds.
        """
        self.webhookurl = config_obj.get("Slack", "webhookurl")

    def slack_pour(self, tap_id, volume_poured, beverage_name, volume_remaining, temperature=None):
        """
        Composes the slack message and passes it to the function that actually connects to slack and slacks.

        :param tap_id: tap ID number
        :param volume_poured: float
        :param beverage_name: string
        :param volume_remaining: float
        :param temperature: float
        :return: nothing
        """
        msg = "I just poured " + volume_poured + " from tap " + str(tap_id) + " (" + volume_remaining + "% remaining) "
        if temperature is not None:
            msg = msg + "at " + str(temperature) + DEGREES + "."
        else:
            msg = msg + "."

        
        self.post_slack(msg)
        return msg

    def post_slack(self,msg):
        """
        Sends a string message to slack to post.

        :param slack: string.
        :return: nada
        """

        slack_data = {'text': msg}

        response = requests.post(
            self.webhookurl, data=json.dumps(slack_data),
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



if __name__ == "__main__":
  CONFIG_FILE = "./config/config.ini"
  config = ConfigParser.ConfigParser()
  config.read(CONFIG_FILE)
  s = SlackNotify(config)
  s.post_slack("test message sent from slack_notify.py")
