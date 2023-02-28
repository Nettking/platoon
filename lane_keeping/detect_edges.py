"""
This function applies a series of image processing steps to detect the edges of the lane lines in a video frame. 

Parameters:
frame (cv2.VideoCapture(0).read()): The input video frame.

Returns:
numpy.ndarray: The binary image with detected edges.

"""

import cv2

def detect_edges(frame):

    # Convert the color image to grayscale
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to the grayscale image
    blur = cv2.GaussianBlur(img, (5,5), 0)

    # Apply Canny edge detection to the blurred image
    edges = cv2.Canny(blur, 100, 200)

    return edges
