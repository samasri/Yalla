import sys

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
    if int(seq) != self.stopSeqCounter: raise Exception('Error: stop_times.txt is not ordered by sequence!')
    else: self.stopTimes[seq] = stopTime
