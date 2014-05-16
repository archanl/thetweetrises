echo "Killing old servers if any"
./killserver.sh
echo "Starting servers..."
node app.js > /dev/null 2>&1 &
python tweet_stream.py > /dev/null 2>&1 &
python tweet_categorize.py > /dev/null 2>&1 &
python trending_streams.py > /dev/null 2>&1 &
echo "Done starting servers..."

