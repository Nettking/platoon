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
from init import *
from platooning import *
from Platoon import *
from PlatoonVehicle import follow_lane

video, gpg, myDistanceSensor = init()


# Create an instance of PlatoonVehicle class
vehicle = PlatoonVehicle(speed=100, distance=10)

# Set up the video capture
cap = cv2.VideoCapture(0)  # Change the number if you have multiple cameras

while True:
    # Capture a video frame
    ret, frame = cap.read()

    # Call the follow_lane method on the vehicle instance
    vehicle.follow_lane(frame, vehicle.gpg)
    control_speed(myDistanceSensor, vehicle.gpg)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()