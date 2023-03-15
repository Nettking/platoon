from PlatoonVehicle import *

# Create an instance of PlatoonVehicle class
vehicle = PlatoonVehicle()
video = vehicle.video


while True:
    try:
        # Read a video frame from the camera
        ret,frame = video.read()

        try:
            data, x_offset, y_offset = vehicle.locateQR(frame)
            vehicle.printQRData(data, x_offset, y_offset)
            steering_angle = vehicle.calculate_steering_angle(x_offset)
            vehicle.steer_robot(steering_angle, vehicle.gpg)


        except:
            print('No QR Found')
            
        vehicle.follow_lane(frame, vehicle.gpg)
        vehicle.control_speed(vehicle.distance_sensor, vehicle.gpg)

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

