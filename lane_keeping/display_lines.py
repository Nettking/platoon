

"""
The `display_lines` function takes a video frame, an array of line segments, and optional line color and line width as input, and returns a new video frame with the detected lines displayed.

Parameters:
frame (cv2.VideoCapture(0).read()): The input video frame.
lines (numpy.ndarray): The array of line segments as endpoints.
line_color (tuple): The RGB color of the lines to be drawn. Default is green.
line_width (int): The width of the lines to be drawn. Default is 6.

Returns:
numpy.ndarray: The output video frame as a NumPy array with the detected lines displayed.


The `display_heading_line` function takes a video frame, a steering angle, and optional line color and line width as input, and returns a new video frame with the heading line displayed.

Parameters:
frame (cv2.VideoCapture(0).read()): The input video frame.
steering_angle (float): The steering angle in degrees.
line_color (tuple): The RGB color of the heading line to be drawn. Default is red.
line_width (int): The width of the heading line to be drawn. Default is 5.

Returns:
frame (cv2.VideoCapture(0).read()): The input video frame with the heading line displayed.
"""

import numpy as np
import cv2
import math

def display_lines(frame, lines, line_color=(0, 255, 0), line_width=6):
    
    '''
    line_image initializes a new NumPy array with zeros having the same shape as the input video frame. 
    The resulting line_image array will be used to draw the detected lane lines and will have the same dimensions as the input frame. 
    '''
    line_image = np.zeros_like(frame)
    
    # Draw lines on the line image using the OpenCV line() function.
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)

    # Combine the line image with the original frame using the OpenCV addWeighted() function.
    line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)

    return line_image


def display_heading_line(frame, steering_angle, line_color=(0, 0, 255), line_width=5 ):

    heading_image = np.zeros_like(frame)  # Create a black image of the same size as the input frame.
    height, width, _ = frame.shape  # Get the height and width of the input frame.

    # Convert the steering angle from degrees to radians.
    steering_angle_radian = steering_angle / 180.0 * math.pi

    # Calculate the endpoints of the heading line using basic trigonometry.
    x1 = int(width / 2)  # The starting x-coordinate is the center of the frame.
    y1 = height  # The starting y-coordinate is the bottom of the frame.
    x2 = int(x1 - height / 2 / math.tan(steering_angle_radian))  # The ending x-coordinate is determined by the steering angle.
    y2 = int(height / 2)  # The ending y-coordinate is the middle of the frame.

    # Draw the heading line on the black image using OpenCV.
    cv2.line(heading_image, (x1, y1), (x2, y2), line_color, line_width)

    # Add the heading line image to the input frame using alpha blending.
    heading_image = cv2.addWeighted(frame, 0.8, heading_image, 1, 1)

    # Return the output video frame with the heading line displayed.
    return heading_image
