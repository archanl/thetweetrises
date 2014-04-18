sudo su -

apt-get install python-software-properties
apt-add-repository ppa:chris-lea/node.js
apt-get update

apt-get install redis-server

apt-get install nodejs

npm install socket.io express redis

pip install -r pip-reqs.txt

python -m textblob.download_corpora

mkdir logs

