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

# Beans
import cv2
import time
from easygopigo3 import EasyGoPiGo3


from lane_keeping import *
from platooning import get_distance

# Initialize GoPiGo3 robot and set speed
gpg = EasyGoPiGo3()
gpg.set_speed(100)

# Initialize video capture and set resolution
video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH,320)
video.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
'''
# Create a platoon of 6 vehicles
platoon = Platoon(6)

# Set the speed and distance of each vehicle
platoon.set_speed(0, 60)
platoon.set_distance(0, 0)
platoon.set_distance(1, 10)
platoon.set_distance(2, 20)
platoon.set_distance(3, 30)
platoon.set_distance(4, 40)
platoon.set_distance(5, 50)

# Find the leader of the platoon
leader_index = platoon.get_leader()
leader = platoon.vehicles[leader_index]

# Print the index and distance of the leader
print("Leader index:", leader_index)
print("Leader distance:", leader.distance)
'''



# Loop through video frames
while True:
    try:
        # Read a video frame from the camera
        ret,frame = video.read()
        

        # Detect edges in the video frame
        edges = detect_edges(frame)
        
        # Select region of interest in the video frame
        roi = region_of_interest(edges)

        # Display edges detected in cropped video frame in new window
        cv2.imshow("Edges in roi", roi)
        
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

        # Display final video with heading line in new window
        cv2.imshow("Heading line", heading_image)
        
        # Output the validated steering angle and wheel speeds to the console
        print('Steering angle:' + str(validated_steering_angle))
        print('Wheel speeds: ' + str(leftSpeed) + str(rightSpeed))

        #print('Distance: ' + get_distance(gpg))
        key = cv2.waitKey(1)
        if key == 27:
            break
    except:
        gpg.set_speed(0)
    
# Stop the robot when the loop is ended
gpg.set_speed(0)

# Release the video capture and close all windows
video.release()
cv2.destroyAllWindows()
