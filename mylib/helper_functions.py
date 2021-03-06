from math import sin, cos, sqrt, atan2, radians
import sys

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
def calculateDistance(lat1,lon1, lat2,lon2):
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


def minRecord(obj1, obj2):
    if obj1.distance < obj2.distance: return obj1
    else: return obj2