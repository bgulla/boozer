#!/usr/bin/python
# -*- coding: utf-8 -*
import tweepy
import sys
import ConfigParser

DEGREES="°"

class TwitterNotify():
  def __init__(self, config_obj):
    self.consumer_key = config_obj.get("Twitter", "consumer_key").strip('"')
    self.consumer_secret = config_obj.get("Twitter", "consumer_secret").strip('"')
    self.access_token = config_obj.get("Twitter", "access_token").strip('"')
    self.access_token_secret = config_obj.get("Twitter", "access_token_secret").strip('"')


  def tweet_pour(self,tap_id, volume_poured, beverage_name, volume_remaining, temperature):
    msg = "I just poured " + volume_poured + " of " + beverage_name + " from tap " + str(tap_id) + " (" + volume_remaining + "% remaining) at " + str(temperature) + DEGREES
    self.post_tweet(msg)

  def post_tweet(self,tweet):
    auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
    auth.set_access_token(self.access_token, self.access_token_secret)
    api = tweepy.API(auth)
    #print "Successfully logged in as " + api.me().name + "."
    try:
      if len(tweet) <= 140:
        api.update_status(tweet)
    #    print "Successfully tweeted: " + "'" + tweet + "'!"
      else:
        raise IOError
    except:
      print "Something went wrong: either your tweet was too long or you didn't pass in a string argument at launch."
