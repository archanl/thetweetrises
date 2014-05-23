import ast
import urllib 

def getTrends(r):
    result = []
    topics = r.zrevrange("trending_keys", 0, 11)
    for topic in topics:
        result.append(topic)
    return result

def classifyTrending(tweet, trends):
    for trend in trends:
        if trend in tweet or urllib.unquote(trend).decode('utf8') in tweet:
            return trend
    else:
        return None


