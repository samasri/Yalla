#!/usr/bin/env bash

../getDistances.py testingMode > result &
PID=$!
sleep 5
kill $PID
./compare.py result
EXIT_CODE=$?
if [ "$EXIT_CODE" == "1" ]; then
    echo "Failed"
else
    echo "Passed!"
    rm result
fi