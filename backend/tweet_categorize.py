import sys
from textblob import TextBlob
import redis
import json
from multiprocessing import Pool
import signal
import logging

# Log everything, and send it to stderr.
logging.basicConfig(level=logging.DEBUG)

QUEUE_KEY = 'tweet_queue'
SENTIMENT_KEY = 'sentiment_stream'
NUM_PROCESSES = 1
MAX_SENTIMENTS = 10000

def signal_handler(signum = None, frame = None):
    logging.debug("Recieved signal " + str(signum))
    logging.debug("Stopping tweet consumer.")
    exit(0)

def main():
    logging.debug("Starting tweet consumer.")

    for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
        signal.signal(sig, signal_handler)

    r = redis.Redis('localhost')
    
    # p = Pool(NUM_PROCESSES)
    # p.map(consume, [r for i in range(NUM_PROCESSES)])
    


# def consume(r):
    while True:
        try:
            if r.llen(SENTIMENT_KEY) >= MAX_SENTIMENTS:
                r.rpop(SENTIMENT_KEY)
                continue

            tweet = json.loads(r.brpop(QUEUE_KEY)[1])

            if tweet['geo'] is None:
                # No geo data? IGNORE!
                continue

            coordinates = tweet['geo']['coordinates']
            sentiment = TextBlob(tweet['text']).sentiment.polarity
            if sentiment != 0:
                # Jsonify tweet with sentiment and store in redis
                d = {'sentiment' : sentiment, \
                     'latitude' : coordinates[0], \
                     'longitude' : coordinates[1] }
                j = json.dumps(d)

                r.lpush(SENTIMENT_KEY, str(j))
        except Exception as e:
            logging.exception("Something awful happened!")

if __name__ == '__main__':
    main()
