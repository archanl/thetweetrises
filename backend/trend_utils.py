def getTrends(r):
    result = []
    topics = r.zrevrangebyscore("trending_keys", "+inf", "-inf", start=0, num=11)
    for topic in topics:
        topic = ast.literal_eval(topic)
        topic = topic['name']
        result.append(topic)
    return result

def classify(tweet, trends):
    for trend in trends:
        if trend in tweet:
            return trend
    else:
        return None


