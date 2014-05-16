apt-get install -y python-software-properties

add-apt-repository -y ppa:rwky/redis
apt-add-repository -y ppa:chris-lea/node.js

apt-get update
apt-get upgrade
apt-get dist-upgrade

aptitude update
aptitude upgrade
aptitude dist-upgrade


apt-get install -y vim redis-server nodejs python-pip build-essential python-sklearn

npm install socket.io express redis node-static underscore

pip install -r pip-reqs.txt

python -m textblob.download_corpora


mkdir logs

