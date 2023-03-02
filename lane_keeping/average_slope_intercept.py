"""
This function takes an array of line segments as input and returns an array of lane lines as output.

Parameters:
frame (cv2.VideoCapture(0).read()): The input video frame.
line_segments (numpy.ndarray): The array of line segments as endpoints.

Returns:
list: The list of lane lines as arrays of endpoints.
"""

import numpy as np
import lane_keeping.make_points as m_p
from easygopigo3 import EasyGoPiGo3

gpg = EasyGoPiGo3()

def average_slope_intercept(frame, line_segments):

    # Initialize the list of lane lines
    lane_lines = []

    # If no line segments were detected, stop the robot and return an empty list of lane lines
    if line_segments is None:
        print("no line segments detected")
        return lane_lines

    # Get the height and width of the input image
    height, width, _ = frame.shape

    # Initialize the lists of left and right line fits
    left_fit = []
    right_fit = []

    # Define the region of interest for the left and right lane lines
    boundary = 1/2
    # The left region of interest is the left half of the image
    left_region_boundary = width * (1 - boundary)
    # Oppsite for right region of interest
    right_region_boundary = width * boundary

    # Iterate over all line segments and fit a line to each segment
    for line_segment in line_segments:
        # Iterate over the endpoints of the line segment
        for x1, y1, x2, y2 in line_segment:
            # Skip vertical lines (slope = infinity)
            if x1 == x2:
                print("skipping vertical lines (slope = infinity")
                continue
            
            # Fit a line to the line segment using linear regression
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            # Calculate the slope and intercept of the line
            slope = (y2 - y1) / (x2 - x1)
            # Calculate the intercept of the line
            intercept = y1 - (slope * x1)
            
            # Classify the line segment as left or right based on the slope and x-coordinate of endpoints
            if slope < 0:
                # If the slope is negative, the line segment is on the left side of the image
                if x1 < left_region_boundary and x2 < left_region_boundary:
                    left_fit.append((slope, intercept))
            else:
                # If the slope is positive, the line segment is on the right side of the image
                if x1 > right_region_boundary and x2 > right_region_boundary:
                    right_fit.append((slope, intercept))

    # Calculate the average slope and intercept for the left and right line fits
    left_fit_average = np.average(left_fit, axis=0)
    # If there are no left line fits, return an empty list of lane lines
    if len(left_fit) > 0:
        # Calculate the endpoints of the left lane line
        lane_lines.append(m_p.make_points(frame, left_fit_average))

    # Repeat for the right lane line
    right_fit_average = np.average(right_fit, axis=0)
    if len(right_fit) > 0:
        lane_lines.append(m_p.make_points(frame, right_fit_average))

    return lane_lines
