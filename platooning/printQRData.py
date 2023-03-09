from platooning import *
def printQRData(data, x_offset, y_offset):
                print('Data: ')
                print(str(data))
                print('X_offset: ')
                print(str(x_offset))
                print('Y_offset: ')
                print(str(y_offset))
                print('Steering Angle: ')
                steering_angle = calculate_steering_angle(x_offset)
                print(str(steering_angle))