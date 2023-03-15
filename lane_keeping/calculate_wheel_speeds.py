import math

# Constants
wheelbase = 0.117  # distance between wheels in meters
max_speed = 100  # maximum speed in meters per second
min_speed = 60  # minimum speed in meters per second

def calculate_wheel_speeds(steering_angle):
    """
    Calculate left and right wheel speeds based on the desired steering angle.

    Parameters:
    steering_angle (float): The desired steering angle in degrees.

    Returns:
    tuple (float, float): The left and right wheel speeds as a tuple.
    """
    
    # Validate steering angle input
    if not 0 <= steering_angle <= 180:
        raise ValueError("Steering angle must be between 0 and 180 degrees")

    # Convert steering angle to radians
    steering_angle_rad = math.radians(steering_angle)

    if abs(steering_angle - 90) < 5:
        # Straight ahead
        left_speed = max_speed
        right_speed = max_speed
    else:
        # Calculate turning radius using small-angle approximation
        turning_radius = wheelbase / steering_angle_rad

        # Calculate turn rate
        turnrate = ((turning_radius - wheelbase / 2) / turning_radius) / 2

        # Calculate wheel speeds based on turning radius
        if steering_angle < 90:
            # Turn right
            left_speed = max_speed * (1 + turnrate)
            right_speed = max_speed * (1 - turnrate)
        else:
            # Turn left
            right_speed = max_speed * (1 + turnrate)
            left_speed = max_speed * (1 - turnrate)

        # Apply speed limits
        left_speed = max(min_speed, min(left_speed, max_speed))
        right_speed = max(min_speed, min(right_speed, max_speed))

    # Return wheel speeds
    return left_speed, right_speed
