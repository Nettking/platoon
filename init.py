import cv2

from math import atan2
from easygopigo3 import EasyGoPiGo3

from lane_keeping import *
from lane_keeping import follow_lane
from platooning import *

def init():
    # Initialize GoPiGo3 robot and set speed
    gpg = EasyGoPiGo3()
    gpg.set_speed(0)

    # Initialize distance sensor
    myDistanceSensor = initialize_distance_sensor(gpg)

    # Initialize video capture and set resolution
    video = cv2.VideoCapture(0)
    video.set(cv2.CAP_PROP_FRAME_WIDTH,320)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
    return video, gpg, myDistanceSensor
