from math import atan2
wheelbase = 0.117  # distance between wheels in meters
max_speed = 100  # maximum speed in meters per second

def calculate_steering_angle(x_offset):
    # Calculate steering angle in radians
    steering_angle = atan2(x_offset, wheelbase/2)*180

    return steering_angle