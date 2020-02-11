# Classes to reproduce the objects obtained from GTFS real time data
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