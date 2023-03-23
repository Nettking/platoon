from PlatoonVehicle import *
import time

# Create an instance of PlatoonVehicle class
vehicle = PlatoonVehicle()

# Initialize GoPiGo3 robot and set speed
gpg = vehicle.gpg
gpg.set_speed(0)
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
#stop_distance = int(input("Please enter stop_distance: "))
#slow_distance = int(input("Please enter slow_distance: "))
while True:
    try:
        # Read a video frame from the camera
        ret,frame = video.read()
        
        try:
            vehicle.follow_qr(frame, gpg)
        except:
            print('No QR Found')
                 
        vehicle.follow_lane(frame, gpg)

    except Exception as e:
        print("An error occurred: {}".format(e))
    try:    
        vehicle.control_speed(gpg, distance_sensor, stop_distance=200, slow_distance=300)

        key = waitKey(1)
        if key == 27:
            vehicle.kill(gpg, video)
            break
    except:
        print('unable to control speed.')

vehicle.kill(gpg, video)


