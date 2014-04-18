import sys
from textblob import TextBlob
import redis
import json
from multiprocessing import Pool

QUEUE_KEY = 'tweet_queue'
SENTIMENT_KEY = 'sentiment_stream'
NUM_PROCESSES = 1
MAX_SENTIMENTS = 10000

def main():
    r = redis.Redis('localhost')
    
    # p = Pool(NUM_PROCESSES)
    # p.map(consume, [r for i in range(NUM_PROCESSES)])
    


# def consume(r):
    while True:
        #try:
        # print r.brpop(QUEUE_KEY)[1]
        tweet = json.loads(r.blpop(QUEUE_KEY)[1])
        if tweet['geo'] is None:
            # No geo data? IGNORE!
            continue
        text = tweet['text']
        coordinates = tweet['geo']['coordinates']
        sentiment = TextBlob(tweet['text']).sentiment.polarity

        # Jsonify tweet with sentiment and store in redis
        d = {'text' : text, \
             'sentiment' : sentiment, \
             'latitude' : coordinates[0], \
             'longitude' : coordinates[1] }
        j = json.dumps(d)

        if r.llen(SENTIMENT_KEY) > MAX_SENTIMENTS:
            r.blpop(SENTIMENT_KEY)

        r.rpush(SENTIMENT_KEY, str(j))

        #except Exception as e:
        #    sys.stderr.write(str(e) + '\n')

if __name__ == '__main__':
    main()
