ps aux | grep "node app.js" | grep -v grep | awk '{print $2}'

