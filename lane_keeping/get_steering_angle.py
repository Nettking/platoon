'''
The get_steering_angle function calculates the steering angle based on the lane lines detected in a video frame. '
The function takes the frame and the detected lane lines as input and returns the steering angle as output.


Parameters:

frame (cv2.VideoCapture(0).read()): The input video frame.
lane_lines (list): A list of lane lines detected in the frame.


Returns:

smooth_angle (float): The calculated steering angle in degrees.
The function first determines the horizontal center of the image and then calculates the x offset from the center of the lane using the end points of the lane lines. 
If only one lane line is detected, the x offset is calculated based on the end points of the line. If no lane lines are detected, the previous steering angle is used.

The function then calculates the angle to the center of the lane and adds 90 degrees to get the steering angle. 
Finally, the steering angle is smoothed using a weighted average of the previous angle and the current angle, with more weight given to the previous angle. 
The smoothed angle is returned as the final steering angle.
'''

import math
last_angle = 90
def get_steering_angle(frame, lane_lines):
    global last_angle
    print('Last Angle: ' + str(last_angle))
    height, width, _ = frame.shape
    
    if len(lane_lines) == 2:
        # Get the end points of both lane lines
        _, _, left_x2, _ = lane_lines[0][0]
        _, _, right_x2, _ = lane_lines[1][0]
        # Get the horizontal center of the image
        mid = int(width / 2)
        # Calculate the x offset from the center of the lane
        x_offset = (left_x2 + right_x2) / 2 - mid
        y_offset = int(height / 2)
        
    elif len(lane_lines) == 1:
        # Get the end points of the lane line
        x1, _, x2, _ = lane_lines[0][0]
        # Calculate the x offset from the center of the lane
        x_offset = x2 - x1
        y_offset = int(height / 2)
        
    elif len(lane_lines) == 0:
        # No lane lines detected, use the previous angle
        x_offset = 0
        y_offset = int(height / 2)
        
    # Calculate the angle to the center of the lane
    angle_to_mid_radian = math.atan(x_offset / y_offset)
    angle_to_mid_deg = int(angle_to_mid_radian * 180.0 / math.pi)  
    steering_angle = angle_to_mid_deg + 90
    
    # Smooth the steering angle
    smooth_angle = (last_angle*2 + steering_angle)/3
    last_angle = smooth_angle
    
    return smooth_angle
