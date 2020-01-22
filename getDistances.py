from google.transit import gtfs_realtime_pb2
import requests
import os
import math
import random
from math import sin, cos, sqrt, atan2, radians
import pathlib

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
    self.stopTimes = [] # List of all StopTime objects
  
  def addStopTime(self,stopTime):
    self.stopTimes.append(stopTime)
  
  # Makes sure all stopTimes are in sequential order
  def checkTrips(self):
    prevSeq = 0
    for stopTime in self.stopTimes:
      if stopTime.sequence < prevSeq: return False
      prevSeq = stopTime.sequence
    return True


# Get information from GTFS data
basePath = str(pathlib.Path(__file__).parent.absolute())
trips = {} # {tripID --> Trip object}
for r in parseCSVtoList(basePath + "/gtfs/trips.txt"): trips[r[2]] = Trip(r[0],r[1],r[2],r[4],r[5])

stops = {} # {stopID --> Stop object}
for r in parseCSVtoList(basePath + "/gtfs/stops.txt"): stops[r[0]] = Stop(r[0],r[1],r[4],r[5])

prevStopSeq = 0
for r in parseCSVtoList(basePath + "/gtfs/stop_times.txt"):
  # Make sure stops are ordered by their sequence for each trip
  stopSeq = len(r[4])
  if stopSeq < prevStopSeq and stopSeq != 1: print('Error: stop_times.txt is not ordered by sequence!')
  prevStopSeq = stopSeq
  stopTime = StopTime(r[0],r[1],r[2],r[3],r[4],r[5],r[8])
  trips[r[0]].addStopTime(stopTime)
  
# Get real-time vehicle positions
feed = gtfs_realtime_pb2.FeedMessage()
response = requests.get('http://rtu.york.ca/gtfsrealtime/VehiclePositions')
feed.ParseFromString(response.content)
limit = int(random.random() * len(feed.entity))
# print("Vehicle ID, Closest Stop ID, Distance")
for vehicle in feed.entity:
  if vehicle.is_deleted: continue
  vehicle = vehicle.vehicle
  vehicleLat = float(vehicle.position.latitude)
  vehicleLon = float(vehicle.position.longitude)
  
  vehicleTrip = trips[vehicle.trip.trip_id]
  vehicleStops = [] # list of Stop objects
  for stopTime in vehicleTrip.stopTimes:
    stopID = stopTime.stop_id
    stop = stops[stopID]
    vehicleStops.append(stop)
  
  # Calculate minimum distance
  closestStop = vehicleStops[0]
  minDistance = calculareDistance(vehicleLat,vehicleLon,closestStop.lat,closestStop.lon)
  for stop in vehicleStops:
    distance = calculareDistance(vehicleLat,vehicleLon,stop.lat,stop.lon)
    if distance < minDistance:
      closestStop = stop
      minDistance = distance
  print("%s,%s,%f" % (vehicle.vehicle.id,closestStop.id,minDistance))


