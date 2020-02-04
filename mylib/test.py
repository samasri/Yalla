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


test_vehicles = [
    Vehicle("V5133", False, "1","1",44.0524,-79.6162), # 105
    Vehicle("V5134", False, "2","1",44.0274,-79.5913), # closer to 105
    Vehicle("V5135", False, "3","1",44.0274,-79.5911), # closer to 104
    Vehicle("V5136", False, "4","1",43.8524,-79.4162), # 101
    Vehicle("V5137", False, "5","1",43.9024,-79.4662), # 102
    Vehicle("V5138", False, "6","1",43.9524,-79.5162), # 103
    Vehicle("V5139", False, "7","1",43.9524,-79.5162), # 103 (supposed to be at 101)
]