from helper_functions import parseCSVtoList
from datetime import timedelta, datetime

class ArrivalTime:
    def __init__(self, arrTime):
        if str.isdigit(arrTime[:2]) and int(arrTime[:2]) >= 24: self.newDay = True
        else: self.newDay = False
        
        arrTime = arrTime.split(':') # By convention, arrival is is HOUR:MINUTE:SECOND
        self.h = int(arrTime[0])
        self.m = int(arrTime[1])
        self.s = int(arrTime[2])
    
    def toDateTime(self,date): # By convention, received date is YEAR-MONTH-DAY
        if self.newDay == 1:
            difference = self.h - 23
            self.h = 23
        arrivalTime = '%d:%d:%d' % (self.h, self.m, self.s)
        time = datetime.strptime(arrivalTime.strip(),"%H:%M:%S")
        dateTime = datetime.combine(date,time.time())
        if self.newDay: dateTime = dateTime + timedelta(hours=difference)
        return dateTime

def buildTripSchedule(path):
    tripSchedule = {} # Trip ID --> Stop Sequence --> Arrival Time
    for r in parseCSVtoList(path):
        tripID = r[0]
        stopSeq = r[4]
        stopID = r[3]
        arrivalTime = r[1].strip()
        if tripID not in tripSchedule: tripSchedule[tripID] = {}
        if stopSeq in tripSchedule[tripID]: print('Trip #%s has two data points for the same sequence (#%s)' % (tripID,stopSeq), file=sys.stderr)
        tripSchedule[tripID][stopSeq] = (stopID,ArrivalTime(arrivalTime))
    return tripSchedule