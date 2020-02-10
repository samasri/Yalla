import sys
from datetime import timedelta, datetime

# struct to hold distance and date
class Record:
    def __init__(self,distance,date):
        self.distance = float(distance) # in meters
        self.timestamp = datetime.strptime(date, "%m/%d/%y--%H:%M:%S") # By convention, coordinated with getDistances.py
        
    def __str__(self):
        return '(%s, %s)' % (self.distance, datetime.strftime(record.timestamp,"%D--%H:%M:%S"))
    
    def __eq__(self, other):
        return str(self) == str(other)

