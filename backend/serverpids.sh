ps aux | grep "node app.js" | grep -v grep | awk '{print $2}'
ps aux | grep "python tweet_stream.py" | grep -v grep | awk '{print $2}'
ps aux | grep "python tweet_categorize.py" | grep -v grep | awk '{print $2}'
