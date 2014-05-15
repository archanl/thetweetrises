kill $(ps aux | grep "node app.js" | grep -v grep | awk '{print $2}')
kill $(ps aux | grep "python tweet_stream.py" | grep -v grep | awk '{print $2}')
kill $(ps aux | grep "python tweet_categorize.py" | grep -v grep | awk '{print $2}')
kill $(ps aux | grep "python trending_streams.py" | grep -v grep | awk '{print $2}')

