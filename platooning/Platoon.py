class PlatoonVehicle:
    def __init__(self, speed, distance):
        
        # Speed of the vehicle
        self.speed = speed

        # Distance of the vehicle from the vehicle in front of it
        self.distance = distance

    def set_speed(self, speed):
        # Set the speed of the vehicle
        self.speed = speed

    def set_distance(self, distance):
        # Set the distance of the vehicle
        self.distance = distance

    def __str__(self):
        # Return a string representation of the vehicle
        return f"Speed: {self.speed}, Distance: {self.distance}"


class Platoon:
    def __init__(self, num_vehicles):
        # Initialize the platoon with the specified number of vehicles
        self.num_vehicles = num_vehicles

        # Create a list of vehicles
        self.vehicles = [PlatoonVehicle(0, 0) for _ in range(num_vehicles)]

    def set_speed(self, vehicle_index, speed):
        # Set the speed of the specified vehicle
        self.vehicles[vehicle_index].speed = speed

    def set_distance(self, vehicle_index, distance):
        # Set the distance of the specified vehicle
        self.vehicles[vehicle_index].distance = distance

    def get_leader(self):
        # Initialize the leader to be the first vehicle
        leader = 0

        # Iterate over the vehicles to find the one with the greatest distance to the vehicle in front of it
        for i in range(1, self.num_vehicles):
            # If the current vehicle is closer to the vehicle in front of it than the current leader, update the leader
            if self.vehicles[i].distance > self.vehicles[leader].distance:
                # Update the leader
                leader = i

        return leader
