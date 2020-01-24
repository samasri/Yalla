#!/usr/bin/env python3

import sys
import os
import collections

# struct to hold distance and date
class Record:
    def __init__(self,distance,date):
        self.distance = distance # in meters
        date = date.split('--') # by convention, -- seperates the date from the time
        self.date = date[0]
        self.time = date[1]
        
    def __str__(self):
        return '(%s, %s, %s)' % (self.distance, self.date, self.time)
    
def minRecord(obj1, obj2):
    if obj1.distance < obj2.distance: return obj1
    # elif obj2.distance < obj1.distance: return obj2
    else: return obj2
    

vehicles = {} # vehicleID --> {tripID --> {stopID --> Record}}
for r in open('results'):
    r = r.strip()
    if not r: continue
    r = r.split(',')
    vehicleID = r[1]
    stopID = r[2]
    record = Record(r[3],r[0])
    tripID = r[4]
    if vehicleID not in vehicles: vehicles[vehicleID] = {}
    if tripID not in vehicles[vehicleID]: vehicles[vehicleID][tripID] = {}
    if stopID in vehicles[vehicleID][tripID]:
        oldRecord = vehicles[vehicleID][tripID][stopID]
        vehicles[vehicleID][tripID][stopID] = minRecord(oldRecord,record)
    else: vehicles[vehicleID][tripID][stopID] = record


distanceFreq = {}
total = 0
for vehicleID, trips in vehicles.items():
    for tripID, stops in trips.items():
        for stopID,record in stops.items():
            total += 1
            print("Bus #%s:" % vehicleID)
            print("Trip ID: %s" % tripID)
            print("Stop ID: %s" % stopID)
            print("Distance from stop: %s" % record.distance)
            print("Timestamp: %s" % record.time)
            distance = int(float(record.distance)/10)
            if distance not in distanceFreq: distanceFreq[distance] = 0
            distanceFreq[distance] += 1


print("Length: " + str(len(vehicles)))

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

