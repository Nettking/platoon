from PlatoonVehicle import *
import time

# Create an instance of PlatoonVehicle class
vehicle = PlatoonVehicle()

# Initialize GoPiGo3 robot and set speed
gpg = vehicle.gpg
vehicle.gpg.set_speed(0)
try:
    # Initialize distance sensor
    distance_sensor = vehicle.distance_sensor
except:
    print('Failed to initialize distance sensor')
# Initialize video capture and set resolution
try:
    video = vehicle.video
except:
    print('Failed to set video')

video.set(CAP_PROP_FRAME_WIDTH,640)
video.set(CAP_PROP_FRAME_HEIGHT,480)

            

time.sleep(1)
while True:
    try:
        # Read a video frame from the camera
        ret,frame = video.read()
        '''
        try:
            data, x_offset, y_offset = vehicle.locateQR(frame)
            vehicle.printQRData(data, x_offset, y_offset)
            steering_angle = vehicle.calculate_steering_angle(x_offset)
            vehicle.steer_robot(steering_angle, gpg)
        except:
            print('No QR Found')
        '''         
        vehicle.follow_lane(frame, gpg)


    except Exception as e:
        print("An error occurred: {}".format(e))
        for item in e.__traceback__:
            print('Trace:' + str(item))
        vehicle.gpg.set_speed(0)
    try:    
        vehicle.control_speed(gpg)

        key = waitKey(1)
        if key == 27:
            break
    except:
        print('unable to control speed.')
# Stop the robot when the loop is ended
vehicle.gpg.set_speed(0)

# Release the video capture and close all windows
video.release()
destroyAllWindows()

