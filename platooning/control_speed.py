from platooning import *

def control_speed(myDistanceSensor, gpg):
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
            else:
                gpg.set_speed(0)
