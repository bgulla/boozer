#!/usr/bin/python
# -*- coding: utf-8 -*
import tweepy
import sys
import ConfigParser
import logging
"""
Boozer library to notify the general public of your drinking habits via Twitter.

"""
# Setup Logging
logger = logging.getLogger(__name__)

# Static vars
DEGREES="°"

class TwitterNotify():

    consumer_key        = None
    consumer_secret     = None
    access_token        = None
    access_token_secret = None

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        """
        Initializes the Twitter client library.

        :param config_obj: SimpleConfig object used to pull the auth creds.
        """
        self.consumer_key       = consumer_key
        self.consumer_secret    = consumer_secret
        self.access_token       = access_token
        self.access_token_secret = access_token_secret

    def post_tweet(self,twitter_status_update):
        """
        Sends a string message to twitter to post.

        :param tweet: string.
        :return: nada
        """
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth)


        logger.info("[Twitter] login successful for %s." % api.me().name)
        logger.info("[Twitter] Attempting to send: %s" % twitter_status_update)
        try:
            if len(twitter_status_update) <= 140:
                api.update_status(twitter_status_update)
                logger.info("[Twitter] Successfully updated status to: %s" % twitter_status_update)
            else:
                raise IOError
        except:
            logger.error("[Twitter] Something went wrong: either your tweet was too long or you didn't pass in a string argument at launch.")
            logger.error(sys.exc_info()[0])

        return twitter_status_update

def main():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.INFO)

    config = ConfigParser.ConfigParser()
    config.read('./config.ini')

    consumer_key = config.get("Twitter", "consumer_key").strip('"')
    consumer_secret = config.get("Twitter", "consumer_secret").strip('"')
    access_token = config.get("Twitter", "access_token").strip('"')
    access_token_secret = config.get("Twitter", "access_token_secret").strip('"')

    client = TwitterNotify(consumer_key, consumer_secret, access_token, access_token_secret)
    client.post_tweet("Test of the twitter_notify.py main method.")

if __name__ == "__main__":
    main()