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

from lane_keeping import lane_keeping
from platooning import *

# Initialize GoPiGo3 robot and set speed
gpg = EasyGoPiGo3()
gpg.set_speed(100)

# Initialize distance sensor
myDistanceSensor = initialize_distance_sensor(gpg)

# Initialize video capture and set resolution
video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH,320)
video.set(cv2.CAP_PROP_FRAME_HEIGHT,240)


# Loop through video frames
while True:
    try:
        # Read a video frame from the camera
        ret,frame = video.read()
        try:
            data, x_offset, y_offset = locateQR(frame, gpg)
            print('Data: ')
            print(str(data))
            print('X_offset: ')
            print(str(x_offset))
            print('Y_offset: ')
            print(str(y_offset))
        except:
            lane_keeping.lane_keeping(frame, gpg)
        
        
        # Get distance and adjust speed if too close
        distance = get_distance(myDistanceSensor)
        if distance is not None:
            print('Distance: ' + distance)
            if int(distance) < 100:
                gpg.set_speed(0)
            elif int(distance) < 200:
                gpg.set_speed(50)
            else:
                gpg.set_speed(100)


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
