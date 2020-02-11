#!/usr/bin/env python3

import sys
from os import listdir
from os.path import isfile, join
import collections
import pathlib
from datetime import timedelta, datetime
from Record import Record, buildRecordsMaps
from StopTime import StopTime
from ArrivalTime import ArrivalTime, buildTripSchedule
from helper_functions import parseCSVtoList, minRecord



# Uses the trip records calculated in `processRecords` to calculate the delays for each trip at the visited stops
def calculateDelays(trips, tripRoutes, tripSchedule):
    delays = {} # Stop ID -> RouteID -> list of delays
    total = 0
    ignored = 0
    for date, tripIDs in trips.items():
        for tripID, stops in tripIDs.items():
            for stopSeq,record in stops.items():
                total += 1
                if record.distance > 20: 
                    ignored += 1
                    continue
                
                stopID = tripSchedule[tripID][stopSeq][0]
                routeID = tripRoutes[tripID]
                deltaTime = record.timestamp - tripSchedule[tripID][stopSeq][1].toDateTime(record.timestamp)

                if stopID not in delays: delays[stopID] = {}
                if routeID not in delays[stopID]: delays[stopID][routeID] = set()
                delays[stopID][routeID].add(deltaTime.total_seconds()/60)
    return delays

def toMySQLStrings(delays):
    results = []
    results.append("CREATE TABLE Delay (stopID INT, routeID VARCHAR(100), delay FLOAT, nbOfData INT);");
    for (stopID,routes) in delays.items():
        for (routeID, delayRecords) in routes.items():
            # Calculate average delay
            avgDelay = sum(delayRecords)/len(delayRecords)
            results.append("INSERT INTO Delay (stopID, routeID, delay, nbOfData) VALUES (%d,\"%s\",%f,%d);" % (int(stopID),routeID,float(avgDelay), len(delayRecords)))
    return results

def processDistances(inp, tripSchedule):
    tripRoutes = {} # Trip ID --> Route ID
    trips = {} # Trip ID --> Stop Sequence --> Record
    trips, tripRoutes = buildRecordsMaps(inp)

    delays = {} # Stop ID -> RouteID -> list of delays
    delays = calculateDelays(trips,tripRoutes, tripSchedule)

    return toMySQLStrings(delays)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Please enter the path to the results file')
        exit(1)
    else: path = sys.argv[1]

    basePath = str(pathlib.Path(__file__).parent.absolute()) + '/..'
    tripSchedule = buildTripSchedule(basePath + "/gtfs/stop_times.txt") # Trip ID --> Stop Sequence --> Arrival Time

    inp = parseCSVtoList(path)
    results = processDistances(inp, tripSchedule)
    for result in results: print(result)