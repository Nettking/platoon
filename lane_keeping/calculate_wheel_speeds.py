"""
calculate_wheel_speeds calculates the left and right wheel speeds based on the desired steering angle.

Parameters:
steering_angle (float): The desired steering angle in degrees.

Returns:
tuple (float, float): The left and right wheel speeds as a tuple.
"""

import math

# Constants
wheelbase = 0.3  # distance between wheels in meters
max_speed = 200  # maximum speed in meters per second

def calculate_wheel_speeds(steering_angle):

    
    # Convert steering angle to radians
    steering_angle_rad = math.radians(steering_angle)

    # Calculate wheel speeds
    if steering_angle >= 85 and steering_angle < 95:
        # Straight ahead
        left_speed = max_speed
        right_speed = max_speed
    else:
        # Calculate turning radius
        turning_radius = wheelbase / math.tan(steering_angle_rad)

        # Calculate wheel speeds based on turning radius
        if steering_angle < 85:
            # Turn left
            left_speed = max_speed
            right_speed = max_speed * (1 - (turning_radius - wheelbase/2) / turning_radius)
        else:
            # Turn right
            right_speed = max_speed
            left_speed = max_speed * (1 - (turning_radius - wheelbase/2) / turning_radius)

    # Apply speed limits
    if left_speed > 100:
        left_speed = 100
    if right_speed > 100:
        right_speed = 100
    if left_speed < 60:
        left_speed = 60
    if right_speed < 60:
        right_speed = 60
    
    # Return wheel speeds
    return left_speed, right_speed
