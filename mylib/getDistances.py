#!/usr/bin/env python3

from google.transit import gtfs_realtime_pb2
import sys
import os
import time
import requests
import pathlib
from Trip import importTrips
from Stop import importStops
from StopTime import importStopTimesToTrips
from helper_functions import calculateDistance

# Takes a list of vehicles from the GTFS real time data and outputs a list of strings,
# each representing a delay for one trip/vehicle
# Print format: Time, Trip ID, Head Sign, Route ID, Stop Sequence, Distance
def processVehicles(vehicles, trips, stops, unknownTrips, errorVehicles):
  results = []
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
    results.append("%s,%s,%s,%s,%s,%f" % (current_time,vehicleTripID,trips[vehicleTripID].headsign, vehicle.trip.route_id,closestSeq,minDistance))
  return results


if __name__ == "__main__":
  basePath = str(pathlib.Path(__file__).parent.absolute()) + '/..'
  trips = importTrips(basePath + "/gtfs/trips.txt") # {tripID --> Trip object}
  stops = importStops(basePath + "/gtfs/stops.txt") # {stopID --> Stop object}
  importStopTimesToTrips(basePath + "/gtfs/stop_times.txt", trips) # fill the trips' "stopTimes" field

  # Collect errors to report them only once
  unknownTrips = set() # trips not found in the database
  errorVehicles = set() # Errorneous vehicle ids

  while True:
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get('http://rtu.york.ca/gtfsrealtime/VehiclePositions')
    feed.ParseFromString(response.content)
    vehicles = feed.entity

    results = processVehicles(vehicles,trips,stops,unknownTrips,errorVehicles)
    for result in results: print(result)
    time.sleep(30)


