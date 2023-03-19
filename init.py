
from easygopigo3 import EasyGoPiGo3



def initialize_distance_sensor(gpg):
    '''
    Create an instance of the Distance Sensor class.
    I2C1 and I2C2 are just labels used for identifyng the port on the GoPiGo3 board.
    But technically, I2C1 and I2C2 are the same thing, so we don't have to pass any port to the constructor.
    '''
    my_distance_sensor = gpg.init_distance_sensor()
    return my_distance_sensor


def init():
    # Initialize GoPiGo3 robot and set speed
    gpg = EasyGoPiGo3()
    gpg.set_speed(0)

    # Initialize distance sensor
    myDistanceSensor = initialize_distance_sensor(gpg)

    # Initialize video capture and set resolution
    video = VideoCapture(0)
    video.set(CAP_PROP_FRAME_WIDTH,640)
    video.set(CAP_PROP_FRAME_HEIGHT,480)
    if video.isOpened() == False:
        print("Error opening video stream or file")
        raise Exception("Error opening video stream or file")
        
    return video, gpg, myDistanceSensor
