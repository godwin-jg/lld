from abc import ABC, abstractmethod
from enum import Enum
import threading

class VehicleType(Enum):
    MOTORCYCLE = 1
    CAR = 2
    TRUCK = 3

class SpotType(Enum):
    SMALL = 1    # For Motorcycles
    COMPACT = 2  # For Cars
    LARGE = 3    # For Trucks

class Vehicle(ABC):
    def __init__(self, license_plate, vehicle_type):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type

class Motorcycle(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.MOTORCYCLE)

class Car(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate, VehicleType.CAR)

class Truck(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.TRUCK)
    

class ParkingSpot:
    def __init__(self, spot_id, spot_type):
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.vehicle = None
        
    def is_available(self):
        return self.vehicle is None
    
    def assign_vehicle(self, vehicle):
        self.vehicle = vehicle
    
    def remove_vehicle(self):
        self.vehicle = None

class ParkingFloor:
    def __init__(self, floor_number, total_spots):
        self.floor_number = floor_number
        self.spots = []
        self._initialize_spots(total_spots)
    
    def _initialize_spots(self, total_spots):
        for i in range(total_spots):
            if i < 3:
                self.spots.append(ParkingSpot(i + 1, SpotType.SMALL))
            elif i < 6:
               self.spots.append(ParkingSpot(i + 1, SpotType.COMPACT))
            else:
                self.spots.append(ParkingSpot(i + 1, SpotType.LARGE))
    
    def _get_matching_spot_type(self, vehicle_type):
        if vehicle_type == VehicleType.MOTORCYCLE: return SpotType.SMALL
        if vehicle_type == VehicleType.CAR: return SpotType.COMPACT
        return SpotType.LARGE
    
    def find_and_occupy_spot(self, vehicle : Vehicle):
        target_type = self._get_matching_spot_type(vehicle.vehicle_type)
        
        for spot in self.spots:
            if spot.is_available() and spot.spot_type == target_type:
                spot.assign_vehicle(vehicle)
                return spot
        return None

    def free_spot(self, spot_id):
        for spot in self.spots:
                if spot.spot_id == spot_id and not spot.is_available():
                    spot.remove_vehicle()
                    return True
        return False
        
class ParkingLot:
    _instance = None
    _global_lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        with cls._global_lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, num_floors, spots_per_floor):
        if not hasattr(self, 'initialized'):
            self.floors = [ParkingFloor(i + 1, spots_per_floor) for i in range(num_floors)]
            self.initialized = True
    
    def park_vehicle(self, vehicle):
        for floor in self.floors:
           assigned_spot = floor.find_and_occupy_spot(vehicle)
           if assigned_spot:
               return f"SUCCESS: {vehicle.vehicle_type.name} [{vehicle.license_plate}] parked on Floor {floor.floor_number}, Spot {assigned_spot.spot_id}"
        return f"FAILED: No available space for {vehicle.vehicle_type.name} [{vehicle.license_plate}]"
    
    def unpark_vehicle(self, floor_num, spot_id):
        if 0 <= floor_num < len(self.floors):
            if self.floors[floor_num].free_spot(spot_id):
                return f"SUCCESS: Spot {spot_id} on Floor {floor_num} is now completely clear."
        return "ERROR: Invalid spot coordinates or spot was already vacant."
    

parking_lot = ParkingLot(num_floors=2, spots_per_floor=10)
parking_lot2 = ParkingLot(num_floors=1, spots_per_floor=5)
print(parking_lot)
print(parking_lot2)

car_1 = Car("KA-01-AB-1234")
truck_1 = Truck("DL-03-XYZ-9999")
moto_1 = Motorcycle("MH-12-QQ-5555")


print(parking_lot2.park_vehicle(car_1))
print(parking_lot2.park_vehicle(truck_1))
print(parking_lot2.park_vehicle(moto_1))