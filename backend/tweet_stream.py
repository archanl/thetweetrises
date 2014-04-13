import requests
import sys
from requests_oauthlib import OAuth1

def main():
    oauth = OAuth1('ZZQMKjtL8kewgk4001jF8krqx',                             # API Key
                   '4EVEmz1EKPTRmJDpQBSeW5Aldxs7KXbaYw7AJo771kKn12qPp4',    # API secret
                   '16635628-QBipfEYkp3d0TBODdnNMHHM0cLYovy3OjcmsHIvNp',    # Access token
                   '3jMS4f7jbWVDxoq5Gl8sXISEZutCWXrv6rmMUeJe2nPTS')         # Access token secret

    t = requests.get('https://stream.twitter.com/1.1/statuses/filter.json?language=en&locations=-180,-90,180,90',
                     auth=oauth, stream=True)

    while True:
        try:
            tweet = next_tweet(t)
            while "delete" in tweet[:10]:
                tweet = next_tweet(t)
            sys.stderr.write(tweet + '\n')
        except Exception as e:
            print e

def next_tweet(t):
    tweet = ""
    for l in t.iter_content():
        tweet += l
        if '\n' in tweet[-10:]:
            tweet = tweet[:tweet.index('\n')]
            return tweet
    
if __name__ == '__main__':
    main()