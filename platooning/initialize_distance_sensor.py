import easygopigo3 as easy

def initialize_distance_sensor(gpg):
    '''
    Create an instance of the Distance Sensor class.
    I2C1 and I2C2 are just labels used for identifyng the port on the GoPiGo3 board.
    But technically, I2C1 and I2C2 are the same thing, so we don't have to pass any port to the constructor.
    '''
    my_distance_sensor = gpg.init_distance_sensor()
    return my_distance_sensor