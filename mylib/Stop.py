from helper_functions import parseCSVtoList

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

def importStops(path):
    stops = {} # {stopID --> Stop object}
    for r in parseCSVtoList(path):
        stops[r[0]] = Stop(r[0],r[1],r[4],r[5])
    return stops