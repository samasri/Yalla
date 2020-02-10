from helper_functions import parseCSVtoList

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

def importStopTimesToTrips(path,trips):
    for r in parseCSVtoList(path):
        stopTime = StopTime(r[0],r[1],r[2],r[3],r[4],r[5],r[8])
        trips[r[0]].addStopTime(r[4],stopTime)