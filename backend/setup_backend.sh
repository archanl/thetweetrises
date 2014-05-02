sudo su -
cd /
mkdir thetweetrises
cd thetweetrises

apt-get install -y python-software-properties

add-apt-repository -y ppa:rwky/redis
apt-add-repository ppa:chris-lea/node.js

apt-get update

apt-get install -y redis-server

apt-get install nodejs

npm install socket.io express redis node-static

pip install -r pip-reqs.txt

python -m textblob.download_corpora

mkdir logs

