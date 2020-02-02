#!/usr/bin/env python3

import sys
from os import listdir
from os.path import isfile, join
import collections
import pathlib
from datetime import timedelta, datetime

if len(sys.argv) < 2:
    print('Please enter the path to the results file')
    exit(1)
else: path = sys.argv[1]

# Parse a CSV file into a list of rows
def parseCSVtoList(f):
  result = []
  for r in open(f):
    r = r.strip()
    if not r: continue
    r = r.split(',')
    result.append(r)
  return result[1:] # Remove header row

# struct to hold distance and date
class Record:
    def __init__(self,distance,date):
        self.distance = float(distance) # in meters
        self.timestamp = datetime.strptime(date, "%m/%d/%y--%H:%M:%S") # By convention, coordinated with getDistances.py
        
    def __str__(self):
        return '(%s, %s)' % (self.distance, datetime.strftime(record.timestamp,"%D--%H:%M:%S"))
    
    def __eq__(self, other):
        return str(self) == str(other)

class ArrivalTime:
    def __init__(self, arrTime):
        if str.isdigit(arrTime[:2]) and int(arrTime[:2]) >= 24: self.newDay = True
        else: self.newDay = False
        
        arrTime = arrTime.split(':') # By convention, arrival is is HOUR:MINUTE:SECOND
        self.h = int(arrTime[0])
        self.m = int(arrTime[1])
        self.s = int(arrTime[2])
    
    def toDateTime(self,date): # By convention, received date is YEAR-MONTH-DAY
        if self.newDay == 1:
            difference = self.h - 23
            self.h = 23
        arrivalTime = '%d:%d:%d' % (self.h, self.m, self.s)
        time = datetime.strptime(arrivalTime.strip(),"%H:%M:%S")
        dateTime = datetime.combine(date,time.time())
        # if self.newDay == 1:
        #     print("Received: " + str(date))
        #     print("Time: " + str(time))
        #     print("Combined: " + str(dateTime))
        if self.newDay: dateTime = dateTime + timedelta(hours=difference)
        return dateTime

def minRecord(obj1, obj2):
    if obj1.distance < obj2.distance: return obj1
    else: return obj2

basePath = str(pathlib.Path(__file__).parent.absolute())

tripSchedule = {} # Trip ID --> Stop Sequence --> Arrival Time
for r in parseCSVtoList(basePath + "/gtfs/stop_times.txt"):
    tripID = r[0]
    stopSeq = r[4]
    stopID = r[3]
    arrivalTime = r[1].strip()
    if tripID not in tripSchedule: tripSchedule[tripID] = {}
    if stopSeq in tripSchedule[tripID]: print('Trip #%s has two data points for the same sequence (#%s)' % (tripID,stopSeq), file=sys.stderr)

    # if str.isdigit(arrivalTime[:2]) and int(arrivalTime[:2]) >= 24: continue
    tripSchedule[tripID][stopSeq] = (stopID,ArrivalTime(arrivalTime))

delays = {}
tripRoutes = {} # Trip ID --> Route ID
vehicles = {} # Trip ID --> Stop Sequence --> Record
for r in open(join(path)):
    r = r.strip()
    if not r: continue
    r = r.split(',')
    tripID = r[1]
    headsign = r[2]
    routeID = r[3]
    stopSeq = r[4]
    record = Record(r[5],r[0]) # A Record constructor takes distance and time

    tripRoutes[tripID] = routeID + ' ' + headsign

    if tripID not in vehicles: vehicles[tripID] = {}
    if stopSeq in vehicles[tripID]:
        oldRecord = vehicles[tripID][stopSeq]
        vehicles[tripID][stopSeq] = minRecord(oldRecord,record) # keep the data where the vehicle is closest to the stop
    else: vehicles[tripID][stopSeq] = record

total = 0
ignored = 0
for tripID, stops in vehicles.items():
    for stopSeq,record in stops.items():
        total += 1
        if record.distance > 20: 
            ignored += 1
            continue
        
        stopID = tripSchedule[tripID][stopSeq][0]
        routeID = tripRoutes[tripID]
        deltaTime = record.timestamp - tripSchedule[tripID][stopSeq][1].toDateTime(vehicles[tripID][stopSeq].timestamp)

        if stopID not in delays: delays[stopID] = {}
        if routeID not in delays[stopID]: delays[stopID][routeID] = set()
        delays[stopID][routeID].add(deltaTime.total_seconds()/60)

# Print MySQL code
print("CREATE TABLE Delay (stopID INT, routeID VARCHAR(50), delay FLOAT, nbOfData INT);");
for (stopID,routes) in delays.items():
    for (routeID, delayRecords) in routes.items():
        # Calculate average delay
        avgDelay = sum(delayRecords)/len(delayRecords)
        print("INSERT INTO Delay (stopID, routeID, delay, nbOfData) VALUES (%d,\"%s\",%f,%d);" % (int(stopID),routeID,float(avgDelay), len(delayRecords)))