"""
This function compares the input value to the last stored value and returns the input value if the difference between the two is less than 100, otherwise it returns the last stored value. The function stores the input value as the last value after comparing.

Parameters:
value (int or float): The input value to be compared to the last stored value.

Returns:
int or float: The input value if the difference between the input value and the last stored value is less than 100, otherwise the last stored value.

"""


# Initialize the last stored value as 90 degrees. 90 +- 100 = 190/-10, which is outside the range of possible steering angles
# However after the first call to compare_to_last_value, the last stored value will be updated to the input value
last_value = 90

# If a value is greater than 100 away from the last stored value, it is likely an outlier and should be ignored
def compare_to_last_value(value):
    # Import the global variable last_value
    global last_value
    
    # Calculate the difference between the input value and the last stored value
    diff = abs(last_value - value)
    
    # Compare the difference to a threshold of 100
    if diff < 100:
        # Store the input value as the last value
        last_value = value
        # Return the input value
        return value
    
    if diff > 100:
        # Store the input value as the last value
        last_value = value
        # Return the last stored value
        return last_value

# Outlier filter