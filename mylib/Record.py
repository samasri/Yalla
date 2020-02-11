from datetime import datetime
from helper_functions import minRecord

# struct to hold distance and date
class Record:
    def __init__(self,distance,date):
        self.distance = float(distance) # in meters
        self.timestamp = datetime.strptime(date, "%m/%d/%y--%H:%M:%S") # By convention, coordinated with getDistances.py
        
    def __str__(self):
        return '(%s, %s)' % (self.distance, datetime.strftime(record.timestamp,"%D--%H:%M:%S"))
    
    def __eq__(self, other):
        return str(self) == str(other)

# Processes the input file (which is outputted from mylib.getDistances). Returns:
# 1. Mapping between each tripID visited by a vehicle in the input file, the stop sequences 
# corresponding to that trip, and the record (a struct of distance and time) of that vehicle to that stop
# 2. Mapping between each tripID and the routeID that trip belongs to
def buildRecordsMaps(inp):
    tripRoutes = {} # Trip ID --> Route ID
    trips = {} # Trip ID --> Stop Sequence --> Record
    for r in inp:
        tripID = r[1]
        headsign = r[2]
        routeID = r[3]
        stopSeq = r[4]
        dateTime = r[0]
        date = dateTime[:dateTime.index('--')]
        distance = r[5]
        record = Record(distance,dateTime) # A Record constructor takes distance and time

        tripRoutes[tripID] = routeID + ' ' + headsign

        if date not in trips: trips[date] = {}
        if tripID not in trips[date]: trips[date][tripID] = {}
        if stopSeq in trips[date][tripID]:
            oldRecord = trips[date][tripID][stopSeq]
            trips[date][tripID][stopSeq] = minRecord(oldRecord,record) # keep the data where the vehicle is closest to the stop
        else: trips[date][tripID][stopSeq] = record
    return trips,tripRoutes