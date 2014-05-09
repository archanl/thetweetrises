import sys
import redis
import requests
from requests_oauthlib import OAuth1
import json
import dateutil.parser as dp

USA_WOEID = '23424977'
TRENDING_KEY = 'trending_keys'
MAX_TRENDING = 10

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

    j_str = ""
    for x in t:
        j_str += x
    j = json.loads(j_str)

    trending_time = j[0]['created_at']
#     if not r.exists(trending_key):
#         while r.llen(TRENDING_KEYS_KEY) >= MAX_TRENDING:
#             to_remove = r.brpop(TRENDING_KEYS_KEY)
# 
#         r.lpush(TRENDING_KEYS_KEY, trending_key)
#         for trend in j[0]['trends']:
#             r.lpush(trending_key, json.dumps(trend))

    epoch = dp.parse(trending_time)
    epoch = epoch.strftime("%s")

    for trend in j[0]['trends']:
        r.zadd(TRENDING_KEY, trend, epoch)

    r.set('trending_json', j_str)


if __name__ == '__main__':
    main()
