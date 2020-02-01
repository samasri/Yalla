#!/usr/bin/env bash

if [ "$1" == "stop" ]; then
    kill -9 $(pgrep python3)
else 
    while true; do
       DATE=$(date '+%F')
       touch /home/samasri/yalla/results/$DATE /home/samasri/yalla/results-err/$DATE
      /home/samasri/yalla/getDistances.py 60 >> /home/samasri/yalla/results/$DATE 2>> /home/samasri/yalla/results-err/$DATE
    done
fi
