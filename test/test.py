#!/usr/bin/env python3
import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).parent.absolute()) + '/../mylib')
from Trip import importTrips
from Stop import importStops
from StopTime import importStopTimesToTrips
from ArrivalTime import buildTripSchedule
from getDistances import processVehicles
from processDistances import processDistances
 
class PositionRecord:
    def __init__(self,lon,lat):
        self.longitude = lon
        self.latitude = lat
class TripRecord:
    def __init__(self, trip_id, route_id):
        self.trip_id = trip_id
        self.route_id = route_id
class SubSubVehicle:
    def __init__(self,id):
        self.id = id
class SubVehicle:
    def __init__(self,trip_id,route_id,lon,lat,vehicle_id):
        self.trip = TripRecord(trip_id,route_id)
        self.position = PositionRecord(lon,lat)
        self.vehicle = SubSubVehicle(vehicle_id)

class Vehicle:
    def __init__(self,vehicle_id, isDeleted,trip_id,route_id,lat,lon):
        self.id = vehicle_id
        self.is_deleted = False
        self.vehicle = SubVehicle(trip_id,route_id,lon,lat,self.id)

def testGetDistanceInstance(vehicle, correctResult,trips,stops,unknownTrips,errorVehicles):
    result = processVehicles([vehicle],trips,stops,unknownTrips,errorVehicles)
    return correctResult in result[0]

def testGetDistance():
    # Mapping between the test name and a tuple of a vehicle data point and the correct result
    # {testName -> [vehicle,correctResult]}
    testCases = {
        "Finding the right stop" : [Vehicle("V5133", False, "1","1",44.0524,-79.6162),"1,head,1,5,0.000000"],
        "Calculating distance corner case 1" : [Vehicle("V5134", False, "2","1",44.0274,-79.5913),"2,head,1,5,3420.009862"],
        "Calculating distance corner case 2" : [Vehicle("V5135", False, "3","1",44.0274,-79.5911),"3,head,1,4,3420.498875"],
        "Very far away from stop" : [Vehicle("V5139", False, "7","1",43.9524,-79.5162),",Markham,1,1,13709.506679"]
    }

    # Global variables used by the test function
    basePath = str(pathlib.Path(__file__).parent.absolute())
    trips = importTrips(basePath + "/gtfs/trips.txt") # {tripID --> Trip object}
    stops = importStops(basePath + "/gtfs/stops.txt") # {stopID --> Stop object}
    importStopTimesToTrips(basePath + "/gtfs/stop_times.txt", trips) # fill the trips' "stopTimes" field

    # Collect errors to report them only once
    unknownTrips = set() # trips not found in the database
    errorVehicles = set() # Errorneous vehicle ids

    result = True
    for (testName, testInfo) in testCases.items():
        currentResult = testGetDistanceInstance(testInfo[0],testInfo[1],trips,stops,unknownTrips,errorVehicles)
        if not currentResult: print ("Test Failed: %s" % testName)
        result &= currentResult

    if result: print("getDistance tests passed!")

def testProcessDistances():
    basePath = str(pathlib.Path(__file__).parent.absolute()) + '/..'
    tripSchedule = buildTripSchedule(basePath + "/gtfs/stop_times.txt") # Trip ID --> Stop Sequence --> Arrival Time

    results = processDistances(basePath + '/test/processDistancesTest', tripSchedule)
    # for result in results: print(result)

testGetDistance()
testProcessDistances()