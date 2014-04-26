node app.js > /dev/null 2>&1 &
python tweet_stream.py > /dev/null 2>&1 &
python tweet_categorize.py > /dev/null 2>&1 &

