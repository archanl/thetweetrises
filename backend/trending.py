import sys
import redis
import requests
from requests_oauthlib import OAuth1

USA_WOEID = '23424977'

def main():
    r = redis.Redis('localhost')

    oauth = OAuth1('ZZQMKjtL8kewgk4001jF8krqx',                             # API Key
                   '4EVEmz1EKPTRmJDpQBSeW5Aldxs7KXbaYw7AJo771kKn12qPp4',    # API secret
                   '16635628-QBipfEYkp3d0TBODdnNMHHM0cLYovy3OjcmsHIvNp',    # Access token
                   '3jMS4f7jbWVDxoq5Gl8sXISEZutCWXrv6rmMUeJe2nPTS')         # Access token secret

    # Trending Topics
    # Place: USA (woeid = 23424977)
    t = requests.get('https://api.twitter.com/1.1/trends/place.json?id=' + USA_WOEID,
                     auth=oauth)

    print t
    
if __name__ == '__main__':
    main()
