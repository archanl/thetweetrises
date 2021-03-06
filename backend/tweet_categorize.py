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
import urllib

# Log everything, and send it to stderr.
logging.basicConfig(level=logging.DEBUG)

TWEET_QUEUE_KEY = 'tweet_queue'
TRENDING_TOPICS_KEY = 'trending_keys'
ALL_SENTIMENTS_KEY = 'sentiment_stream'
PERMANENT_TOPICS_KEY = 'permanent_topics'
TOPIC_SENTIMENTS_KEY_PREFIX = 'topic_sentiment_stream:'

MAX_SENTIMENTS = 10000
UPDATE_INT = 40 # seconds. Update interval for trending topics

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
    
    f = open("../NLP/Wrapper/test.txt", 'rb')
    p = cPickle.load(f)
    f.close()

    last_updated = None

    sentiment_queue_size = r.zcard(ALL_SENTIMENTS_KEY)

    while True:
        try:
            # Update topics and trends every UPDATE_INT seconds
            if last_updated is None or time.time() - last_updated > UPDATE_INT:
                permanent_topics_json = r.get(PERMANENT_TOPICS_KEY)
                if permanent_topics_json:
                    permanent_topics = json.loads(permanent_topics_json)
                else:
                    permanent_topics = []

                all_trending_keywords = r.zrange(TRENDING_TOPICS_KEY, 0, -1)
                trending_keywords = all_trending_keywords[-12:]
                removing_trending_keywords = all_trending_keywords[:-12]
                r.delete(*[TOPIC_SENTIMENTS_KEY_PREFIX + topic for topic in removing_trending_keywords])

                last_updated = time.time()

                for topic in permanent_topics:
                    r.zremrangebyscore(TOPIC_SENTIMENTS_KEY_PREFIX + topic, "-inf", last_updated - 86400)
                for topic in trending_keywords:
                    r.zremrangebyscore(TOPIC_SENTIMENTS_KEY_PREFIX + topic, "-inf", last_updated - 86400)



            # Get tweet
            tweet_json = r.rpop(TWEET_QUEUE_KEY)
            if not tweet_json:
                time.sleep(1)
                continue
            tweet = json.loads(tweet_json)


            # Get Sentiment
            sentiment_classification = p.classify(tweet['text'], "naive_bayes", 0.5)
            if sentiment_classification == "positive":
                sentiment = 1
            elif sentiment_classification == "negative":
                sentiment = -1
            else:
                sentiment = 0


            # Format sentiment point correctly and put into correct queue
            if sentiment != 0:
                # Get coordinates
                if tweet['geo'] is not None:
                    latitude, longitude = tweet['geo']['coordinates']
                else:
                    latitude, longitude = None, None


                # Get topic
                topics = None

                for trend in trending_keywords:
                    trend_decoded = urllib.unquote(trend).decode('utf8')
                    if (trend in tweet['text']) or (trend_decoded in tweet['text']):
                        if topics is None:
                            topics = []
                        topics.append(trend_decoded)

                for topic in permanent_topics:
                    for topic_keyword in permanent_topics[topic]:
                        topic_keyword_decoded = urllib.unquote(topic_keyword).decode('utf8')
                        if (topic_keyword in tweet['text']) or (topic_keyword_decoded in tweet['text']):
                            if topics is None:
                                topics = []
                            topics.append(topic)
                            break

                # Format sentiment point
                sentiment_point_timestamp = time.time()
                sentiment_point = {'topic': None, 'latitude': latitude, 'longitude': longitude, 'sentiment': sentiment, 'timestamp': sentiment_point_timestamp}

                # Put into general sentiment queue
                if sentiment_queue_size >= MAX_SENTIMENTS:
                    r.zremrangebyrank(ALL_SENTIMENTS_KEY, 0, 0)
                    sentiment_queue_size -= 1

                r.zadd(ALL_SENTIMENTS_KEY, json.dumps(sentiment_point), sentiment_point_timestamp)
                sentiment_queue_size += 1


                # Belongs to topics? Put into correct queue
                if topics is not None:
                    for topic in topics:
                        sentiment_point['topic'] = topic
                        r.zadd(TOPIC_SENTIMENTS_KEY_PREFIX + topic, json.dumps(sentiment_point), sentiment_point_timestamp)

        except Exception as e:
            logging.exception("Something awful happened!")

if __name__ == '__main__':
    main()
