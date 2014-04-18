node app.js >> logs/app.log 2>&1 &
python tweet_stream.py >> logs/tweet_stream.log 2>&1 &
python tweet_categorize.py >> logs/tweet_categorize.log 2>&1 &

