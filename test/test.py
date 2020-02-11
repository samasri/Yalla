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
from TestingClasses import Vehicle

def testGetDistanceInstance(vehicle, correctResult,trips,stops,unknownTrips,errorVehicles):
    result = processVehicles([vehicle],trips,stops,unknownTrips,errorVehicles)
    return correctResult in result[0]

def testProcessDistancesInstance(inp,correctResult,tripSchedule):
    for i in range(len(inp)): inp[i] = inp[i].split(',')
    results = processDistances(inp,tripSchedule)[1:] # remove CREATE stmt
    return set(correctResult) == set(results)

def testGetDistance():
    # Mapping between the test name and its input data
    testCases = {
        "Finding the right stop" : Vehicle("V5133", False, "1","1",44.0524,-79.6162),
        "Calculating distance corner case 1" : Vehicle("V5134", False, "2","1",44.0274,-79.5913),
        "Calculating distance corner case 2" : Vehicle("V5135", False, "3","1",44.0274,-79.5911),
        "Very far away from stop" : Vehicle("V5139", False, "7","1",43.9524,-79.5162)
    }
    # Mapping between the test name and the correct result
    correctResults = {
        "Finding the right stop" : "1,head,1,5,0.000000",
        "Calculating distance corner case 1" : "2,head,1,5,3420.009862",
        "Calculating distance corner case 2" : "3,head,1,4,3420.498875",
        "Very far away from stop" : ",Markham,1,1,13709.506679"
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
        currentResult = testGetDistanceInstance(testInfo,correctResults[testName],trips,stops,unknownTrips,errorVehicles)
        if not currentResult: print ("Test Failed: %s" % testName)
        result &= currentResult

    if result: print("All getDistances tests passed!")

def testProcessDistances():
    basePath = str(pathlib.Path(__file__).parent.absolute()) + '/..'
    tripSchedule = buildTripSchedule(basePath + "/gtfs/stop_times.txt") # Trip ID --> Stop Sequence --> Arrival Time

    testCases = {
        "Triple records" : [
            "02/07/20--06:33:13,1401566,Finch Terminal - MO,302,40,10.000000",
            "02/07/20--06:34:13,1401566,Finch Terminal - MO,302,40,5.000000",
            "02/07/20--06:34:13,1401566,Finch Terminal - MO,302,40,15.000000"
        ],
        "Same stop and trip, different day" : [
            "02/07/20--06:32:13,1401566,Finch Terminal - MO,302,39,0.000000",
            "02/07/21--06:33:13,1401566,Finch Terminal - MO,302,39,0.000000"
        ],
        "Arriving early" : [
            "02/07/20--07:53:13,1401565,Finch Terminal - MO,302,41,0.000000"
        ],
        "Very far away from stop" : [
            "02/07/23--07:35:13,1401567,Finch Terminal - MO,302,40,3000.000000"
        ]
    }

    correctResults = {
        "Triple records" : [
            'INSERT INTO Delay (stopID, routeID, delay, nbOfData) VALUES (3157,"302 Finch Terminal - MO",2.216667,1);'
        ],
        "Same stop and trip, different day" : [
            'INSERT INTO Delay (stopID, routeID, delay, nbOfData) VALUES (3155,"302 Finch Terminal - MO",2.100000,2);'
        ],
        "Arriving early" : [
            'INSERT INTO Delay (stopID, routeID, delay, nbOfData) VALUES (2331,"302 Finch Terminal - MO",-1.783333,1);'
        ],
        "Very far away from stop" : []
    }

    result = True
    for (testName, testInput) in testCases.items():
        currentResult = testProcessDistancesInstance(testInput,correctResults[testName],tripSchedule)
        if not currentResult: print("Test Failed: %s" % testName)
        result &= currentResult
    if result: print ("All processDistances tests passed!")

testGetDistance()
testProcessDistances()