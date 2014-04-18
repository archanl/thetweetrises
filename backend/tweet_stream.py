import sys
import redis
import requests
from requests_oauthlib import OAuth1

MAXQUEUESIZE = 10000
QUEUE_KEY = 'tweet_queue'

def main():
    r = redis.Redis('localhost')

    oauth = OAuth1('ZZQMKjtL8kewgk4001jF8krqx',                             # API Key
                   '4EVEmz1EKPTRmJDpQBSeW5Aldxs7KXbaYw7AJo771kKn12qPp4',    # API secret
                   '16635628-QBipfEYkp3d0TBODdnNMHHM0cLYovy3OjcmsHIvNp',    # Access token
                   '3jMS4f7jbWVDxoq5Gl8sXISEZutCWXrv6rmMUeJe2nPTS')         # Access token secret

    # language: English
    # location bounding box: USA
    t = requests.get('https://stream.twitter.com/1.1/statuses/filter.json?language=en&locations=-125.0011,24.9493,-66.9326,49.5904',
                     auth=oauth, stream=True)

    while True:
        #try:
        if r.llen(QUEUE_KEY) < MAXQUEUESIZE:
            tweet = next_tweet(t)
            while "delete" in tweet[:10]:
                tweet = next_tweet(t)
            r.lpush(QUEUE_KEY, tweet)


        #except Exception as e:
        #    sys.stderr.write(str(e) + '\n')

def next_tweet(t):
    tweet = ""
    for l in t.iter_content():
        tweet += l
        if '\n' in tweet[-10:]:
            tweet = tweet[:tweet.index('\n')]
            return tweet
    
if __name__ == '__main__':
    main()
