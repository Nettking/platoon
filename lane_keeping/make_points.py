"""
Compute the endpoints of a line segment that extends from the bottom of
the frame to the middle of the frame, given the parameters of a line in
slope-intercept form.

Args:
    frame: The input image as a numpy array.
    line: A tuple (slope, intercept) representing a line in slope-
            intercept form.

Returns:
    A list of two points [x1, y1, x2, y2] representing the endpoints of
    the line segment.
"""


def make_points(frame, line):
 
    # Get the height and width of the input frame
    height, width, _ = frame.shape
    
    # Unpack the slope and intercept of the line
    slope, intercept = line
    
    # Calculate the y-coordinates of the endpoints of the line
    y1 = height  # bottom of the frame
    y2 = int(y1 / 2)  # make points from middle of the frame down
    
    # Handle the case where the slope is zero
    if slope == 0:
        slope = 0.1
        
    # Calculate the x-coordinates of the endpoints of the line using the
    # slope-intercept form of a line
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    
    # Return the endpoints of the line as a list of two points
    return [[x1, y1, x2, y2]]
