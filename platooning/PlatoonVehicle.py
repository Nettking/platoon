class PlatoonVehicle:
    def __init__(self, id):
        
        # Speed of the vehicle
        self.speed = 0
        # Set id of the vehicle
        self.id = id

    def set_speed(self, speed):
        # Set the speed of the vehicle
        self.speed = speed

    def set_distance(self, distance):
        # Set the distance of the vehicle in front of this vehicle
        self.distance = distance

    def adjust_speed(distance, min_distance=100, max_distance=100000, max_speed=100):
        """
        Adjust the speed of the vehicle based on the distance to a vehicle ahead.

        Args:
            distance: The distance to the vehicle ahead, in millimeters.
            min_distance: The minimum safe distance to maintain, in millimeters.
                            Default is 100 millimeters (10 centimeters).
            max_distance: The maximum safe distance to maintain, in millimeters.
                            Default is 110 millimeters (11 centimeters).
            max_speed: The maximum speed of the vehicle, in % of the maximum speed.
                        Default is 100 %

        Returns:
            A value between 0 and 100 indicating the speed to set, where 0 means
            the vehicle should be stopped and 100 means the vehicle should travel
            at the maximum speed.
        """
        # Convert the distances to meters
        distance = distance / 1000.0
        min_distance = min_distance / 1000.0
        max_distance = max_distance / 1000.0

        # Calculate the speed factor based on the distance to the vehicle ahead
        if distance <= min_distance:
            speed_factor = 0.0  # Stop the vehicle
        elif distance >= max_distance:
            speed_factor = 1.0  # Travel at the maximum speed
        else:
            speed_factor = (distance - min_distance) / (max_distance - min_distance)

        # Calculate the speed to set based on the maximum speed of the vehicle
        speed = speed_factor * max_speed

        # Return the speed as an integer between 0 and 100
        return int(round(speed))
    
    def __str__(self):
        # Return a string representation of the vehicle
        return f"Speed: {self.speed}, Distance: {self.distance}"
