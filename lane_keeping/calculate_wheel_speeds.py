"""
calculate_wheel_speeds calculates the left and right wheel speeds based on the desired steering angle.

Parameters:
steering_angle (float): The desired steering angle in degrees.

Returns:
tuple (float, float): The left and right wheel speeds as a tuple.
"""

import math

# Constants
wheelbase = 0.117  # distance between wheels in meters
max_speed = 100  # maximum speed in meters per second

def calculate_wheel_speeds(steering_angle):

    # Validate steering angle input
    if not 0 <= steering_angle <= 180:
        raise ValueError("Steering angle must be between 0 and 180 degrees")

    # Convert steering angle to radians and assign maximum speed to a variable
    steering_angle_rad = math.radians(steering_angle)
    max_speed = 100

    # Calculate wheel speeds
    if abs(steering_angle - 90) < 1e-6:
        # Straight ahead
        left_speed = right_speed = max_speed
    else:
        # Calculate turning radius and wheel speeds based on turning radius
        turning_radius = wheelbase / math.sin(steering_angle_rad)
        turning_factor = (turning_radius - wheelbase/2) / turning_radius
        # Calculate left and right wheel speeds
        left_speed = max_speed * (1 - turning_factor * math.cos(steering_angle_rad/2))
        right_speed = max_speed * (1 - turning_factor * math.cos((180-steering_angle_rad)/2))

    # Apply speed limits
    left_speed = max(60, min(left_speed, 100))
    right_speed = max(60, min(right_speed, 100))

    # Return wheel speeds
    return left_speed, right_speed
