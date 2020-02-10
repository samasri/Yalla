from helper_functions import parseCSVtoList

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

def importTrips(path):
    trips = {} # {tripID --> Trip object}
    for r in parseCSVtoList(path):
        trips[r[2]] = Trip(r[0],r[1],r[2],r[3],r[5])
    return trips