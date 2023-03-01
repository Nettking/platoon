import PlatoonVehicle

class Platoon:
    def __init__(self, num_vehicles):
        self.num_vehicles = num_vehicles

        # Create a list of vehicles
        self.vehicles = [PlatoonVehicle(i) for i in range(num_vehicles)]

        # Set the speed of all vehicles to 0
        self.speed = 0
        

    def set_speed(self, vehicle_index, speed):
        self.vehicles[vehicle_index].speed = speed

    def set_distance(self, vehicle_index, distance):
        self.vehicles[vehicle_index].distance = distance

    def get_leader(self):
        # Initialize the leader to be the first vehicle
        leader = 0

        # Iterate over the vehicles to find the one with the greatest distance to the vehicle in front of it
        for i in range(1, self.num_vehicles):
            if self.vehicles[i].distance > self.vehicles[leader].distance:
                leader = i

        return leader
