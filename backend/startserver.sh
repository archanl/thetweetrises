node app.js &> /dev/null &
python tweet_stream.py &> logs/tweet_stream.log &
python tweet_categorize.py &> logs/tweet_categorize.log &

