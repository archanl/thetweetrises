import sys
import redis
import requests
from requests_oauthlib import OAuth1
import logging
import signal
import time
from trend_utils import getTrends, classifyTrending

# Log everything, and send it to stderr.
logging.basicConfig(level=logging.DEBUG)

MAXQUEUESIZE = 10000
MAX_TWEET_CACHE = 1
QUEUE_KEY = 'trending_raw'
UPDATE_INT = 20

def signal_handler(signum = None, frame = None):
    logging.debug("Received signal " + str(signum))
    logging.debug("Stopping tweet streamer.")
    exit(0)

def main():
    logging.debug("Starting tweet streamer.")

    #for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
    # On Windows, signal() can only be called with SIGABRT, SIGFPE, SIGILL, SIGINT, SIGSEGV, or SIGTERM. 
    # A ValueError will be raised in any other case.
    for sig in [signal.SIGTERM, signal.SIGINT]:
        signal.signal(sig, signal_handler)

    r = redis.Redis('localhost')

    trends = getTrends(r)

    t = generateRequest(trends)


    while True:
        try:
            if int(time.time()) % UPDATE_INT == 0:
                # Update the trends
                trends = getTrends(r)
                t = generateRequest(trends)

            if t.status_code != 200:
                continue
                
            tweet = next_tweet(t)
    #             while "delete" in tweet[:10]:
    #                 tweet = next_tweet(t)

            r.lpush(QUEUE_KEY, tweet)

        except Exception, e:
            logging.debug(e)


def generateRequest(trends):
    oauth = OAuth1('ZZQMKjtL8kewgk4001jF8krqx',                             # API Key
                   '4EVEmz1EKPTRmJDpQBSeW5Aldxs7KXbaYw7AJo771kKn12qPp4',    # API secret
                   '16635628-QBipfEYkp3d0TBODdnNMHHM0cLYovy3OjcmsHIvNp',    # Access token
                   '3jMS4f7jbWVDxoq5Gl8sXISEZutCWXrv6rmMUeJe2nPTS')         # Access token secret

    # language: English
    # location bounding box: USA
    trends = ",".join(trends)
    t = requests.get('https://stream.twitter.com/1.1/statuses/filter.json?language=en&track=' + trends,
                     auth=oauth, stream=True)
    return t

    

def next_tweet(t):
    tweet = ""
    for l in t.iter_content():
        tweet += l
        if '\n' in tweet[-10:]:
            tweet = tweet[:tweet.index('\n')]
            return tweet
    
if __name__ == '__main__':
    main()
