import sys
from textblob import TextBlob
import redis
import json
from multiprocessing import Pool
import signal
import logging
import cPickle
import sys
sys.path.insert(0, '../NLP/Wrapper/')
sys.path.insert(0, '../NLP/')
sys.path.insert(0, '../NLP/NaiveBayes')
sys.path.insert(0, '../NLP/MaximumEntropy')
sys.path.insert(0, '../NLP/StochasticGradientDescent')
sys.path.insert(0, '../NLP/SupportVectorMachine')
from wrapper import classifier_wrapper, tweetclass
from trend_utils import getTrends, classifyTrending
import time
from dateutil import parser

# Log everything, and send it to stderr.
logging.basicConfig(level=logging.DEBUG)

QUEUE_KEY = 'tweet_queue'
SENTIMENT_KEY = 'sentiment_stream'
NUM_PROCESSES = 1
MAX_SENTIMENTS = 10000
UPDATE_INT = 4 # Update interval for trending topics
TRENDING_KEY = "trending_raw"

def signal_handler(signum = None, frame = None):
    logging.debug("Recieved signal " + str(signum))
    logging.debug("Stopping tweet consumer.")
    exit(0)

def main():
    logging.debug("Starting tweet consumer.")

    #for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
    # On Windows, signal() can only be called with SIGABRT, SIGFPE, SIGILL, SIGINT, SIGSEGV, or SIGTERM. 
    # A ValueError will be raised in any other case.
    for sig in [signal.SIGTERM, signal.SIGINT]:
        signal.signal(sig, signal_handler)

    r = redis.Redis('localhost')
    
    # p = Pool(NUM_PROCESSES)
    # p.map(consume, [r for i in range(NUM_PROCESSES)])
    


# def consume(r):
    f = open("../NLP/Wrapper/test.txt", 'rb')
    p = cPickle.load(f)
    f.close()
    trends = getTrends(r)

    while True:
        try:
            if int(time.time()) % UPDATE_INT == 0:
                trends = getTrends(r)

            if r.zcard(SENTIMENT_KEY) >= MAX_SENTIMENTS:
                r.rpop(SENTIMENT_KEY)
                continue


            # TODO: DRY this

            # Categorize and store trending topics
            tweet = json.loads(r.brpop(TRENDING_KEY)[1])
            if tweet['geo'] is None:
                # No geo data? IGNORE!
                continue

            coordinates = tweet['geo']['coordinates']
            times = tweet['created_at']
            times = parser.parse(times).strftime("%s")

            sentiment = p.classify(tweet['text'], "naive_bayes", 0.5)
            if sentiment == "positive":
                sentiment = 1
            elif sentiment == "negative":
                sentiment = -1
            elif sentiment == "neutral":
                sentiment = 0
            if sentiment != 0:
                # Jsonify tweet with sentiment and store in redis
                d = {'sentiment' : sentiment, \
                     'latitude' : coordinates[0], \
                     'longitude' : coordinates[1], \
                     'timestamp' : times }
                logging.debug("data from categorizer: ")
                logging.debug(d)
                j = json.dumps(d)

                key = classifyTrending(tweet['text'], trends)
                if key != None:
                    r.zadd("trending:" + key, str(j), times)
                else:
                    logging.exception("Key for tweet: " + str(tweet) + " with text: " + text + "was none." + "Trends: " + ", ".join(trends))


                

            tweet = json.loads(r.brpop(QUEUE_KEY)[1])

            if tweet['geo'] is None:
                # No geo data? IGNORE!
                continue

            coordinates = tweet['geo']['coordinates']
            times = tweet['created_at']
            times = parser.parse(times).strftime("%s")

            '''
            sentiment = TextBlob(tweet['text']).sentiment.polarity
            if sentiment != 0:
                # Jsonify tweet with sentiment and store in redis
                d = {'sentiment' : sentiment, \
                     'latitude' : coordinates[0], \
                     'longitude' : coordinates[1] }
                logging.debug("data from categorizer: ")
                logging.debug(d)
                j = json.dumps(d)

                r.lpush(SENTIMENT_KEY, str(j))
                '''
            sentiment = p.classify(tweet['text'], "naive_bayes", 0.5)
            if sentiment == "positive":
                sentiment = 1
            elif sentiment == "negative":
                sentiment = -1
            elif sentiment == "neutral":
                sentiment = 0
            if sentiment != 0:
                # Jsonify tweet with sentiment and store in redis
                d = {'sentiment' : sentiment, \
                     'latitude' : coordinates[0], \
                     'longitude' : coordinates[1], \
                     'timestamp' : times }
                logging.debug("data from categorizer: ")
                logging.debug(d)
                j = json.dumps(d)

                r.zadd(SENTIMENT_KEY, str(j), times)
        except Exception as e:
            logging.exception("Something awful happened!")

if __name__ == '__main__':
    main()
