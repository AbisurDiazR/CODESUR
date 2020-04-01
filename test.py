from TwitterAPI import TwitterAPI

consumer_key = 'gsswiM06At2InB2hgzwfpAiVO'
consumer_secret = 'jvt4RD4s6rzCUbRq4cCQWTS0dwg809TieyIUpPj2kV1UViuqbt'
access_token = '2460423055-aoTaKilqm8RCiwXWXg5d9L0Y3JF6rhVnDA5jpLl'
access_token_secret = '5IuyQNSDleh6PkS1HXSE8N1Au30JgoLhHoj9QtiI3pMhd'

api = TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)

r = api.request('search/tweets',{'q':'ai shinozaki gravure idol'})
for item in r:
    print('<--------------------->')
    print(item['created_at'] + ' <-> ' + item['text'] + ' <-> ' +item['user']['screen_name'])