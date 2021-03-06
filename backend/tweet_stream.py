import sys
import redis
import requests
from requests_oauthlib import OAuth1
import logging
import signal
import datetime
import json
import urllib
import time

# Log everything, and send it to stderr.
logging.basicConfig(level=logging.DEBUG)

MAXQUEUESIZE = 10000
QUEUE_KEY = 'tweet_queue'

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

    oauth = OAuth1('ZZQMKjtL8kewgk4001jF8krqx',                             # API Key
                   '4EVEmz1EKPTRmJDpQBSeW5Aldxs7KXbaYw7AJo771kKn12qPp4',    # API secret
                   '16635628-QBipfEYkp3d0TBODdnNMHHM0cLYovy3OjcmsHIvNp',    # Access token
                   '3jMS4f7jbWVDxoq5Gl8sXISEZutCWXrv6rmMUeJe2nPTS')         # Access token secret

    last_updated = None
    t = None

    while True:
        try:
            if last_updated is None or time.time() - last_updated > 40:
                last_updated = time.time()
                if t:
                    t.close()
                t = generateRequest(r, oauth)

            tweet = next_tweet(t)
            while "delete" in tweet[:10]:
                tweet = next_tweet(t)

            r.lpush(QUEUE_KEY, tweet)

        except Exception as e:
            logging.debug("Something awful happened!")

def generateRequest(r, oauth):
    print "GENERATING REQUEST!!!!!!!!!!!"
    permanent_topics_json = r.get("permanent_topics")
    print permanent_topics_json
    if permanent_topics_json:
        permanent_keywords = [urllib.quote(item) for sublist in json.loads(permanent_topics_json).values() for item in sublist]
    else:
        permanent_keywords = []

    trending_keywords = r.zrevrange("trending_keys", 0, 11)
    print trending_keywords
    keywords = ",".join(permanent_keywords + trending_keywords)

    t = requests.get('https://stream.twitter.com/1.1/statuses/filter.json?' + \
                     'language=en&' + \
                     'locations=-125.0011,24.9493,-66.9326,49.5904&' + \
                     'track=' + keywords, \
                     auth=oauth, \
                     stream=True)
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
