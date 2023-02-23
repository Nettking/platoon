"""
This function applies the probabilistic Hough transform to the binary image with detected edges to detect line segments. 

Parameters:
cropped_edges (numpy.ndarray): The binary image with detected edges within the region of interest.

Returns:
numpy.ndarray: The array of line segments as endpoints.
"""

import numpy as np
import cv2

def detect_line_segments(cropped_edges):
    
    # Set the distance resolution of the Hough grid in pixels
    rho = 1
    
    # Set the angle resolution of the Hough grid in radians
    theta = np.pi / 180  
    
    # Set the threshold for line detection in Hough space
    min_threshold = 10  
    
    # Apply the probabilistic Hough transform to the input image to detect line segments
    line_segments = cv2.HoughLinesP(cropped_edges, rho, theta, min_threshold, 
                                    np.array([]), minLineLength=40, maxLineGap=80)
    
    return line_segments
