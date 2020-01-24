#!/usr/bin/env python3

import sys
from os import listdir
from os.path import isfile, join
import collections
import pathlib
from datetime import timedelta, datetime


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
        self.distance = distance # in meters
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
        dateTime = datetime.strptime(date.strip() + '--' + arrivalTime.strip(),"%Y-%m-%d--%H:%M:%S")
        if self.newDay: dateTime = dateTime + timedelta(hours=difference)
        return dateTime

def minRecord(obj1, obj2):
    if obj1.distance < obj2.distance: return obj1
    # elif obj2.distance < obj1.distance: return obj2
    else: return obj2

basePath = str(pathlib.Path(__file__).parent.absolute())

tripSchedule = {} # Trip ID --> Stop Sequence --> Arrival Time
for r in parseCSVtoList(basePath + "/gtfs/stop_times.txt"):
    tripID = r[0]
    stopSeq = r[4]
    stopID = r[3]
    arrivalTime = r[1].strip()
    if tripID not in tripSchedule: tripSchedule[tripID] = {}
    if stopSeq in tripSchedule[tripID]: print('Error: %s - %s' % (tripID,stopSeq), file=sys.stderr)

    # if str.isdigit(arrivalTime[:2]) and int(arrivalTime[:2]) >= 24: continue
    tripSchedule[tripID][stopSeq] = (stopID,ArrivalTime(arrivalTime))

for f in listdir(join(basePath,'results')):
    currentDate = f # file is called after the date it represents
    vehicles = {} # Trip ID --> Stop Sequence --> Record
    tripBuses = {}
    for r in open(join(basePath,'results',f)):
        r = r.strip()
        if not r: continue
        r = r.split(',')
        vehicleID = r[1]
        stopID = r[3]
        stopSeq = r[4]
        record = Record(r[5],r[0])
        tripID = r[2]
        if tripID not in tripBuses: tripBuses[tripID] = set()
        tripBuses[tripID].add(vehicleID)
        if vehicleID not in vehicles: vehicles[vehicleID] = {}
        if tripID not in vehicles[vehicleID]: vehicles[vehicleID][tripID] = {}
        if stopSeq in vehicles[vehicleID][tripID]:
            oldRecord = vehicles[vehicleID][tripID][stopSeq]
            vehicles[vehicleID][tripID][stopSeq] = minRecord(oldRecord,record)
        else: vehicles[vehicleID][tripID][stopSeq] = record

    for tripID,buses in tripBuses.items():
        if(len(buses) > 1):
            print("%s --> %s" % (tripID, str(buses)))
    distanceFreq = {}
    total = 0
    for vehicleID, trips in vehicles.items():
        for tripID, stops in trips.items():
            for stopSeq,record in stops.items():
                total += 1
                # print("Bus #%s:" % vehicleID)
                # print("Trip ID: %s" % tripID)
                # print("Stop Sequence: %s" % stopSeq)
                # print("Distance from stop: %s" % record.distance)
                # print("Timestamp: %s" % datetime.strftime(record.timestamp,"%D--%H:%M:%S"))
                deltaTime = record.timestamp - tripSchedule[tripID][stopSeq][1].toDateTime(currentDate)
                # print("Delay: %s" % str(deltaTime))
                distance = int(float(record.distance)/10)
                if distance not in distanceFreq: distanceFreq[distance] = 0
                distanceFreq[distance] += 1

    distanceFreq = sorted(distanceFreq.items(), key=lambda kv: kv[0])
    distanceFreq = collections.OrderedDict(distanceFreq)
    over100 = 0
    for distance,freq in distanceFreq.items():
        distance *= 10
        if distance >= 100:
            over100 += freq
            continue
        print("%s --> %.2f" % (distance,(freq/total*100)))
    print("%s --> %s (%.2f percent)" % ("Over 100",over100,(over100/total*100)))

