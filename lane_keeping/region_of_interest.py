"""
This function applies a region of interest mask to the binary image with detected edges to focus on the lower half of the screen where the lane lines are likely to appear. 

Parameters:
edges (numpy.ndarray): The binary image with detected edges.

Returns:
numpy.ndarray: The binary image with detected edges within the region of interest.

"""

import numpy as np
import cv2

def region_of_interest(edges):

    # Get the height and width of the input image
    height, width = edges.shape
    
    # Create a mask with the same shape as the input image
    mask = np.zeros_like(edges)

    # Define a polygon that outlines the lower half of the image
    polygon = np.array([[
        (0, height),
        (0,  height/3),
        (width , height/3),
        (width , height),
    ]], np.int32)
    
    # Fill the polygon with white color
    cv2.fillPoly(mask, polygon, 255)
    
    # Apply the mask to the input image using bitwise AND operation
    cropped_edges = cv2.bitwise_and(edges, mask)
    
    return cropped_edges
