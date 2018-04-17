#!/usr/bin/python

import tweepy
import sys
import ConfigParser

CONFIG_FILE="config.ini"
config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE)

def post_tweet(tweet):

  consumer_key = config.get("Twitter", "consumer_key").strip('"')
  consumer_secret = config.get("Twitter", "consumer_secret").strip('"')
  access_token = config.get("Twitter", "access_token").strip('"')
  access_token_secret = config.get("Twitter", "access_token_secret").strip('"')
  
  print "Consumer Key:", consumer_key

  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  api = tweepy.API(auth)
  print "Successfully logged in as " + api.me().name + "."
  try:
    if len(tweet) <= 140:
      api.update_status(tweet)
      print "Successfully tweeted: " + "'" + tweet + "'!"
    else:
      raise IOError
  except:
    print "Something went wrong: either your tweet was too long or you didn't pass in a string argument at launch."
  finally:
    print "Shutting down script..."


if __name__ == '__main__':
  post_tweet(sys.argv[1])
