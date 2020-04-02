import GetOldTweets3 as got

tweetCriteria = got.manager.TweetCriteria().setUsername('dania').setSince("2018-05-01").setUntil("2019-05-01").setMaxTweets(500)

#tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]

#print(tweet.text)

for tweet in got.manager.TweetManager.getTweets(tweetCriteria):
    print(tweet.date)
    print("->" + tweet.username)
    print("->" + tweet.text)