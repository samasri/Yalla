#!bin/bash

echo "I am running"
DATE=$(date '+%F')
/home/samasri/yalla/getDistances.py > /home/samasri/yalla/results-$DATE 2> /home/samasri/yalla/results-err-$DATE &
sleep 5 # wait 24 hours
# kill -9 $(pgrep python3)
