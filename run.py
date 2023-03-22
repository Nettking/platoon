from PlatoonVehicle import *

# Create an instance of PlatoonVehicle class
vehicle = PlatoonVehicle()
video, gpg, myDistanceSensor = vehicle.init()

while True:
    try:
        # Read a video frame from the camera
        ret,frame = video.read()

        try:
            data, x_offset, y_offset = vehicle.locateQR(frame)
            #vehicle.printQRData(data, x_offset, y_offset)
            #steering_angle = vehicle.calculate_steering_angle(x_offset)
            #vehicle.steer_robot(steering_angle, gpg)
        except:
            print('No QR Found')
        
        
            
        #vehicle.follow_lane(frame, gpg)
        #vehicle.control_speed(gpg)

        key = waitKey(1)
        if key == 27:
            break

    except:
        print('Unable to follow lane')
        vehicle.gpg.set_speed(0)
    
# Stop the robot when the loop is ended
vehicle.gpg.set_speed(0)

# Release the video capture and close all windows
video.release()
destroyAllWindows()

