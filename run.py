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
from Platoon import *
from PlatoonVehicle import *
from cv2 import waitKey, destroyAllWindows

# Create an instance of PlatoonVehicle class
vehicle = PlatoonVehicle(speed=100, distance=10)
myDistanceSensor = vehicle.distance_sensor
video = vehicle.video
gpg = vehicle.gpg


# Loop through video frames
while True:
    try:
        # Read a video frame from the camera
        ret,frame = video.read()

        try:
            data, x_offset, y_offset = vehicle.locateQR(frame)
            vehicle.printQRData(data, x_offset, y_offset)
            steering_angle = vehicle.calculate_steering_angle(x_offset)
            vehicle.steer_robot(steering_angle, gpg)
 
        except:
            print('No QR Found')
            vehicle.follow_lane(frame, gpg)
        
        vehicle.control_speed(myDistanceSensor, gpg)

        key = waitKey(1)
        if key == 27:
            break

    except:
        gpg.set_speed(0)
    
# Stop the robot when the loop is ended
gpg.set_speed(0)

# Release the video capture and close all windows
video.release()
destroyAllWindows()
