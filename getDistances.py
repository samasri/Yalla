#!/usr/bin/env python3

from google.transit import gtfs_realtime_pb2
import sys
import os
import time
import requests
import pathlib
from datetime import datetime, timedelta
from mylib.test import test_vehicles
from mylib.classes import Stop, StopTime, Trip
from mylib.helper_functions import parseCSVtoList, calculateDistance

testingMode = False
if len(sys.argv) > 1:
  if sys.argv[1] == 'testingMode': testingMode = True

# Get information from GTFS data
basePath = str(pathlib.Path(__file__).parent.absolute())
if testingMode:
  tripsPath = basePath + "/test/gtfs/trips.txt"
  stopsPath = basePath + "/test/gtfs/stops.txt"
  stopTimesPath = basePath + "/test/gtfs/stop_times.txt"
else:
  tripsPath = basePath + "/gtfs/trips.txt"
  stopsPath = basePath + "/gtfs/stops.txt"
  stopTimesPath = basePath + "/gtfs/stop_times.txt"

trips = {} # {tripID --> Trip object}
stops = {} # {stopID --> Stop object}

for r in parseCSVtoList(tripsPath): trips[r[2]] = Trip(r[0],r[1],r[2],r[3],r[5])
for r in parseCSVtoList(stopsPath): stops[r[0]] = Stop(r[0],r[1],r[4],r[5])
for r in parseCSVtoList(stopTimesPath):
  stopTime = StopTime(r[0],r[1],r[2],r[3],r[4],r[5],r[8])
  trips[r[0]].addStopTime(r[4],stopTime)

# Collect errors to report them only once
unknownTrips = set() # trips not found in the database
errorVehicles = set() # Errorneous vehicle ids

while True:
  # Get real-time vehicle positions
  if testingMode: vehicles = test_vehicles
  else:
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get('http://rtu.york.ca/gtfsrealtime/VehiclePositions')
    feed.ParseFromString(response.content)
    vehicles = feed.entity
  for vehicle in vehicles:
    if vehicle.is_deleted: continue
    vehicle = vehicle.vehicle
    vehicleLat = float(vehicle.position.latitude)
    vehicleLon = float(vehicle.position.longitude)
    vehicleTripID = vehicle.trip.trip_id
    
    # Report errors if they haven't appeared before
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
    minDistance = calculateDistance(vehicleLat,vehicleLon,closestStop.lat,closestStop.lon)
    for (seq,stop_time) in vehicleTrip.stopTimes.items():
      stop = stops[stop_time.stop_id]
      distance = calculateDistance(vehicleLat,vehicleLon,stop.lat,stop.lon)
      # print("Vehicle #%s: (%s,%s) -- (%s,%s): %s# Stop"% (vehicle.vehicle.id,vehicleLat,vehicleLon,stop.lat,stop.lon,stop.id))
      if distance < minDistance:
        closestStop = stop
        closestSeq = seq
        minDistance = distance
    
    current_time = time.strftime("%D--%H:%M:%S", time.localtime())
    # Printing: Time, Trip ID, Head Sign, Route ID, Stop Sequence, Distance
    print("%s,%s,%s,%s,%s,%f" % (current_time,vehicleTripID,trips[vehicleTripID].headsign, vehicle.trip.route_id,closestSeq,minDistance), flush=True)
  time.sleep(30)


