import re
import io
import csv
import tweepy
from tweepy import OAuthHandler
# Get Old Tweets
import GetOldTweets3 as got

consumer_key = 'gsswiM06At2InB2hgzwfpAiVO'
consumer_secret = 'jvt4RD4s6rzCUbRq4cCQWTS0dwg809TieyIUpPj2kV1UViuqbt'
access_token = '2460423055-aoTaKilqm8RCiwXWXg5d9L0Y3JF6rhVnDA5jpLl'
access_token_secret = '5IuyQNSDleh6PkS1HXSE8N1Au30JgoLhHoj9QtiI3pMhd'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

users_list = api.search_users('canelones')
user_name = ''
for user in users_list:
   user_name = user.id_str
   print(user.screen_name+"<->"+user.description+"<->"+user.location+"<->"+user.profile_image_url_https)

"""
print("--------------------------------")
print(user_name)
print("--------------------------------")

tweet_criteria = got.manager.TweetCriteria().setUsername(user_name).setMaxTweets(100)
all_tweets = got.manager.TweetManager.getTweets(tweet_criteria)

count = 0
for tweet in tweepy.Cursor(api.user_timeline,id=user_name).items():
   print(str(count)+"<->"+tweet.text)
   count += 1
"""