#!/bin/bash

# from: 
# https://stackoverflow.com/questions/878600/how-to-create-cronjob-using-bash

crontab -l > mycron
echo "* * * * * python /root/thetweetrises/backend/trending.py" >> mycron

crontab mycron
rm mycron
