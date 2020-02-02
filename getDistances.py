#!/usr/bin/env python3

from google.transit import gtfs_realtime_pb2
import sys
import os
import time
import random
import math
from math import sin, cos, sqrt, atan2, radians
import requests
import pathlib
import time
from datetime import datetime, timedelta

# Parse a CSV file into a list of rows
def parseCSVtoList(f):
  result = []
  for r in open(f):
    r = r.strip()
    if not r: continue
    r = r.split(',')
    result.append(r)
  return result[1:] # Remove header row

# Calculates distance between two coordinates
def calculareDistance(lat1,lon1, lat2,lon2):
  # approximate radius of earth in km
  R = 6373.0

  lat1 = radians(lat1)
  lon1 = radians(lon1)
  lat2 = radians(lat2)
  lon2 = radians(lon2)

  dlon = lon2 - lon1
  dlat = lat2 - lat1

  a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  c = 2 * atan2(sqrt(a), sqrt(1 - a))

  distance = R * c * 1000 # in meters
  return distance


# Represents a bus stop
class Stop:
  def __init__(self, stop_id, stop_code, stop_lat, stop_lon):
    self.id = stop_id
    self.code = stop_code
    self.lat = float(stop_lat)
    self.lon = float(stop_lon)
  
  def __str__(self):
    return ("Stop %s: (%s,%s)" % (self.id,self.lat,self.lon))
  
  def toMySQL(self):
    return "INSERT INTO Stop (StopID, lat, lon) VALUES(%d,%f,%f);" % (int(self.id),self.lat,self.lon)

# Links a trip to a stop
class StopTime:
  def __init__(self,trip_id,arrival_time,departure_time,stop_id,sequence,headsign,distance_travelled):
    self.trip_id = trip_id
    self.arrival_time = arrival_time
    self.departure_time = departure_time
    self.stop_id = stop_id
    self.sequence = len(sequence)
    self.headsign = headsign
    self.distance_travelled = distance_travelled # distance travelled so far by the bus

class Trip:
  def __init__(self,route_id,service_id,id,headsign,direction_id):
    self.id = id
    self.route_id = route_id
    self.service_id = service_id
    self.id = id
    self.headsign = headsign # Direction displayed on bus
    self.direction_id = direction_id
    self.stopTimes = {} # Stop Sequence --> StopTime objects
    self.stopSeqCounter = 0 # next expected stop sequence (in addStopTime() function)
  
  def addStopTime(self,seq,stopTime):
    self.stopSeqCounter += 1
    if int(seq) != self.stopSeqCounter: print('Error: stop_times.txt is not ordered by sequence!', file=sys.stderr)
    else: self.stopTimes[seq] = stopTime


# Get information from GTFS data
basePath = str(pathlib.Path(__file__).parent.absolute())
trips = {} # {tripID --> Trip object}
for r in parseCSVtoList(basePath + "/gtfs/trips.txt"): trips[r[2]] = Trip(r[0],r[1],r[2],r[3],r[5])

stops = {} # {stopID --> Stop object}
for r in parseCSVtoList(basePath + "/gtfs/stops.txt"): stops[r[0]] = Stop(r[0],r[1],r[4],r[5])
# for (id,stop) in stops.items(): print (stop.toMySQL())

for r in parseCSVtoList(basePath + "/gtfs/stop_times.txt"):
  stopTime = StopTime(r[0],r[1],r[2],r[3],r[4],r[5],r[8])
  trips[r[0]].addStopTime(r[4],stopTime)

# Collect errors to report them only once
unknownTrips = set() # trips not found in the database
errorVehicles = set() # Errorneous vehicle ids

startTime = datetime.now()
while True:
  # Get real-time vehicle positions
  feed = gtfs_realtime_pb2.FeedMessage()
  response = requests.get('http://rtu.york.ca/gtfsrealtime/VehiclePositions')
  feed.ParseFromString(response.content)
  limit = int(random.random() * len(feed.entity))
  for vehicle in feed.entity:
    if vehicle.is_deleted: continue
    vehicle = vehicle.vehicle
    vehicleLat = float(vehicle.position.latitude)
    vehicleLon = float(vehicle.position.longitude)
    vehicleTripID = vehicle.trip.trip_id
    if vehicleTripID not in trips:
      if vehicleTripID in unknownTrips and vehicle.vehicle.id in errorVehicles: continue
      unknownTrips.add(vehicleTripID)
      errorVehicles.add(vehicle.vehicle.id)
      print("Error, vehicle (#%s) is in an unknown trip (#%s)" % (vehicle.vehicle.id,vehicleTripID), file=sys.stderr)
      continue
    vehicleTrip = trips[vehicleTripID]
    
    # Calculate minimum distance
    closestStop = stops[vehicleTrip.stopTimes["1"].stop_id] # Set to first element by default
    closestSeq = 1
    minDistance = calculareDistance(vehicleLat,vehicleLon,closestStop.lat,closestStop.lon)
    for (seq,stop_time) in vehicleTrip.stopTimes.items():
      stop = stops[stop_time.stop_id]
      distance = calculareDistance(vehicleLat,vehicleLon,stop.lat,stop.lon)
      if distance < minDistance:
        closestStop = stop
        closestSeq = seq
        minDistance = distance
    current_time = time.strftime("%D--%H:%M:%S", time.localtime())
    # Printing: Time, Trip ID, Head Sign, Route ID, Stop Sequence, Distance
    print("%s,%s,%s,%s,%s,%f" % (current_time,vehicleTripID,trips[vehicleTripID].headsign, vehicle.trip.route_id,closestSeq,minDistance))
  time.sleep(30)


