from lane_keeping import *
def steer_robot(steering_angle, gpg):
    # Validate the steering angle by comparing it to the last value
    validated_steering_angle = compare_to_last_value(steering_angle)
    
    # Calculate the wheel speeds based on the validated steering angle
    leftSpeed, rightSpeed = calculate_wheel_speeds(validated_steering_angle)
    
    # Control the robot steering based on the calculated wheel speeds
    gpg.steer(rightSpeed, leftSpeed)