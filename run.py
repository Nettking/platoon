"""
This script uses computer vision techniques to detect and track lane lines
in real-time video and controls the steering of a GoPiGo3 robot using these
detected lane lines. The script uses the OpenCV library to perform image 
processing tasks such as edge detection, region of interest selection,
line segment detection, and line fitting to detect the lane lines in the 
video frames. 

The script also uses functions from external modules such as 
compare_to_last_value.py, detect_edges.py, region_of_interest.py, 
detect_line_segments.py, average_slope_intercept.py, display_lines.py, 
get_steering_angle.py, and calculate_wheel_speeds.py to perform the 
necessary image processing and control the robot steering.

The script displays the lane lines and heading line on the video frames 
and outputs the validated steering angle and wheel speeds to the console 
for debugging purposes.

The script requires the installation of the OpenCV and EasyGoPiGo3 libraries.

"""

import cv2
import time
from easygopigo3 import EasyGoPiGo3

from compare_to_last_value import *
from detect_edges import *
from region_of_interest import *
from detect_line_segments import *
from average_slope_intercept import *
from display_lines import *
from get_steering_angle import *
from calculate_wheel_speeds import *

# Initialize GoPiGo3 robot and set speed
gpg = EasyGoPiGo3()
gpg.set_speed(100)

# Initialize video capture and set resolution
video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH,320)
video.set(cv2.CAP_PROP_FRAME_HEIGHT,240)

# Loop through video frames
while True:
    try:
        # Read a video frame from the camera
        ret,frame = video.read()
        
        # Detect edges in the video frame
        edges = detect_edges(frame)
        
        # Select region of interest in the video frame
        roi = region_of_interest(edges)
        
        # Detect line segments in the selected region of interest
        line_segments = detect_line_segments(roi)
        
        # Fit line segments to obtain the lane lines
        lane_lines = average_slope_intercept(frame,line_segments)
        
        # Display the lane lines on the video frame
        lane_lines_image = display_lines(frame,lane_lines)
        
        # Calculate the steering angle based on the lane lines
        steering_angle = get_steering_angle(frame, lane_lines)
        
        # Validate the steering angle by comparing it to the last value
        validated_steering_angle = compare_to_last_value(steering_angle)
        
        # Calculate the wheel speeds based on the validated steering angle
        leftSpeed, rightSpeed = calculate_wheel_speeds(validated_steering_angle)
        
        # Control the robot steering based on the calculated wheel speeds
        gpg.steer(rightSpeed, leftSpeed) 
        
        # Display the heading line on the video frame
        heading_image = display_heading_line(lane_lines_image, steering_angle)
        
        # Output the validated steering angle and wheel speeds to the console
        print('Steering angle:' + str(validated_steering_angle))
        print('Wheel speeds: ' + str(leftSpeed, rightSpeed))
        
        # Show the video frame with the heading line
        cv2.imshow('Heading line', heading_image)
        
        # Exit the loop if the ESC key is pressed
        key = cv2.waitKey(1)
        if key == 27:
            break
        
        # Wait for a short period of time before processing the next frame
        time.sleep(0.05)
        
    except:
        # Stop the robot if an error occurs
        gpg.set_speed(0)

# Stop the robot when the loop is ended
gpg.set_speed(0)

# Release the video capture and close all windows
video.release()
cv2.destroyAllWindows()
