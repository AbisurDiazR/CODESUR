import re
import io
import csv
import tweepy
from tweepy import OAuthHandler

consumer_key = 'gsswiM06At2InB2hgzwfpAiVO'
consumer_secret = 'jvt4RD4s6rzCUbRq4cCQWTS0dwg809TieyIUpPj2kV1UViuqbt'
access_token = '2460423055-aoTaKilqm8RCiwXWXg5d9L0Y3JF6rhVnDA5jpLl'
access_token_secret = '5IuyQNSDleh6PkS1HXSE8N1Au30JgoLhHoj9QtiI3pMhd'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def get_tweets(query, count = 300):

    #empty list to store parsed tweets
    tweets = []
    target = io.open("myTweets.txt",'w',encoding='utf-8')
    #call twitter api to fetch tweets
    q=str(query)
    a=str(q+" ai shinozaki")
    b=str(q+" gravure")
    c=str(q+" idol")
    fetched_tweets = api.search(a, count = count) + api.search(b, count = count) + api.search(c, count = count)
    #parsing tweets one by one
    print(len(fetched_tweets))
    #print(fetched_tweets)

    for tweet in fetched_tweets:

        print(tweet.text)
        
        #empty dictionary to store required params of a tweet
        parsed_tweet = {}
        #saving text of tweet
        parsed_tweet['user'] = tweet.text
        if "http" not in tweet.text:
            line = re.sub("[^A-Za-z]"," ", tweet.text)
            target.write(line+"\n")
    return tweets

tweets = get_tweets(query=" lesbian ", count=50)