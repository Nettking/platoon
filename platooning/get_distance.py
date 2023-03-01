import time
from platooning import initialize_distance_sensor

def get_distance(my_distance_sensor):
    # Read the distance value from the sensor and return it to a string.
    try:
        # Read the distance value from the sensor and convert it to a string.
        distance_in_mm = str(my_distance_sensor.read_mm())
        
        # Return the distance value
        return distance_in_mm
    
    # If there is an error reading the distance value, print an error message and return None
    except:
        print("Distance sensor reading error")
        return None

if __name__ == '__main__':

    #initialize distance sensor
    my_distance_sensor = initialize_distance_sensor()
    
    # Continue reading the values from the sensor until the user presses CTRL+C
    while True:
        # Read the distance value from the sensor and convert it to a string.
        distance_in_mm = get_distance(my_distance_sensor)

        # Directly print the values of the sensor.
        print("Distance Sensor Reading (mm): " + distance_in_mm)