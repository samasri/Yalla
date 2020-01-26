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
    if stopSeq in tripSchedule[tripID]: print('Trip #%s has two data points for the same sequence (#%s)' % (tripID,stopSeq), file=sys.stderr)

    # if str.isdigit(arrivalTime[:2]) and int(arrivalTime[:2]) >= 24: continue
    tripSchedule[tripID][stopSeq] = (stopID,ArrivalTime(arrivalTime))

for f in listdir(join(basePath,'results')):
    currentDate = f # file is called after the date it represents
    vehicles = {} # Trip ID --> Stop Sequence --> Record
    delays = {}
    for r in open(join(basePath,'results',f)):
        r = r.strip()
        if not r: continue
        r = r.split(',')
        stopSeq = r[3]
        record = Record(r[4],r[0])
        tripID = r[1]
        routeID = r[2]
        if tripID not in vehicles: vehicles[tripID] = {}
        if stopSeq in vehicles[tripID]:
            oldRecord = vehicles[tripID][stopSeq]
            vehicles[tripID][stopSeq] = minRecord(oldRecord,record)
        else: vehicles[tripID][stopSeq] = record

    distanceFreq = {}
    total = 0
    for tripID, stops in vehicles.items():
        for stopSeq,record in stops.items():
            total += 1
            stopID = tripSchedule[tripID][stopSeq][0]
            # print("Trip ID: %s" % tripID)
            # print("Stop Sequence: %s" % stopSeq)
            # print("Distance from stop: %s" % record.distance)
            # print("Timestamp: %s" % datetime.strftime(record.timestamp,"%D--%H:%M:%S"))
            deltaTime = record.timestamp - tripSchedule[tripID][stopSeq][1].toDateTime(currentDate)
            # print("Delay: %s" % str(deltaTime))

            if stopID not in delays: delays[stopID] = {}
            if tripID in delays[stopID]: print('Error: Trip #%s has two records for the same stopID (#%s)' % (tripID,stopID), file=sys.stderr)
            delays[stopID][tripID] = deltaTime.total_seconds()/60
            if delays[stopID][tripID] > 30: print ("%s,%s" % (tripID, stopID))
            distance = int(float(record.distance)/10)
            if distance not in distanceFreq: distanceFreq[distance] = 0
            distanceFreq[distance] += 1
    
    avg = 0
    total = 0
    for (stopID,trips) in delays.items():
        for (tripID, deltaTime) in trips.items():
            avg += deltaTime
            total += 1
    print("Average: %f" % (avg/total))

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

