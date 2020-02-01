#!/usr/bin/env bash


if [ "$1" == "stop" ]; then
    kill -9 $(pgrep python3)
else 
    while true; do
       DATE=$(date '+%F')
       mkdir -p results-err results
       touch results/$DATE results-err/$DATE
       ./getDistances.py 60 >> results/$DATE 2>> results-err/$DATE
    done
fi
