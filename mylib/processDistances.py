#!/usr/bin/env python3

import sys
from os import listdir
from os.path import isfile, join
import collections
import pathlib
from datetime import timedelta, datetime
from Record import Record
from StopTime import StopTime
from ArrivalTime import ArrivalTime, buildTripSchedule
from helper_functions import parseCSVtoList, minRecord

# Processes the input file (which is outputted from getDistances.py). Returns:
# 1. Mapping between each tripID visited by a vehicle in the input file, the stop sequences 
# corresponding to that trip, and the record (a struct of distance and time) of that vehicle to that stop
# 2. Mapping between each tripID and the routeID that trip belongs to
def processResultsFile(path):
    tripRoutes = {} # Trip ID --> Route ID
    trips = {} # Trip ID --> Stop Sequence --> Record
    for r in open(path):
        if '#' in r: r = r[:r.index('#')] # Ignore commas
        r = r.strip()
        if not r: continue
        r = r.split(',')
        tripID = r[1]
        headsign = r[2]
        routeID = r[3]
        stopSeq = r[4]
        record = Record(r[5],r[0]) # A Record constructor takes distance and time

        tripRoutes[tripID] = routeID + ' ' + headsign

        if tripID not in trips: trips[tripID] = {}
        if stopSeq in trips[tripID]:
            oldRecord = trips[tripID][stopSeq]
            trips[tripID][stopSeq] = minRecord(oldRecord,record) # keep the data where the vehicle is closest to the stop
        else: trips[tripID][stopSeq] = record
    return trips,tripRoutes

# Uses the trip records calculated in `processResultsFile` to calculate the delays for each trip at the visited stops
def calculateDelays(trips, tripRoutes, tripSchedule):
    delays = {} # Stop ID -> RouteID -> list of delays
    total = 0
    ignored = 0
    for tripID, stops in trips.items():
        for stopSeq,record in stops.items():
            total += 1
            if record.distance > 20: 
                ignored += 1
                continue
            
            stopID = tripSchedule[tripID][stopSeq][0]
            routeID = tripRoutes[tripID]
            deltaTime = record.timestamp - tripSchedule[tripID][stopSeq][1].toDateTime(trips[tripID][stopSeq].timestamp)

            if stopID not in delays: delays[stopID] = {}
            if routeID not in delays[stopID]: delays[stopID][routeID] = set()
            delays[stopID][routeID].add(deltaTime.total_seconds()/60)
    return delays

def printDelaysSQL(delays):
    results = []
    results.append("CREATE TABLE Delay (stopID INT, routeID VARCHAR(100), delay FLOAT, nbOfData INT);");
    for (stopID,routes) in delays.items():
        for (routeID, delayRecords) in routes.items():
            # Calculate average delay
            avgDelay = sum(delayRecords)/len(delayRecords)
            results.append("INSERT INTO Delay (stopID, routeID, delay, nbOfData) VALUES (%d,\"%s\",%f,%d);" % (int(stopID),routeID,float(avgDelay), len(delayRecords)))
    return results

def processDistances(path, tripSchedule):
    tripRoutes = {} # Trip ID --> Route ID
    trips = {} # Trip ID --> Stop Sequence --> Record
    trips, tripRoutes = processResultsFile(path)

    delays = {} # Stop ID -> RouteID -> list of delays
    delays = calculateDelays(trips,tripRoutes, tripSchedule)

    return printDelaysSQL(delays)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Please enter the path to the results file')
        exit(1)
    else: path = sys.argv[1]

    basePath = str(pathlib.Path(__file__).parent.absolute()) + '/..'
    tripSchedule = buildTripSchedule(basePath + "/gtfs/stop_times.txt") # Trip ID --> Stop Sequence --> Arrival Time

    results = processDistances(path, tripSchedule)
    for result in results: print(result)