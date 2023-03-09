from platooning import *

class PlatoonVehicle:
    def __init__(self, speed, distance, MQTT_TOPIC_SUB = "test/in", MQTT_TOPIC_PUB = "test/out", MQTT_BROKER_PORT = 1883):
        
        # Speed of the vehicle
        self.speed = speed

        # Distance of the vehicle from the vehicle in front of it
        self.distance = distance

        # Unique IP address of the vehicle
        self.unique_ip = ""

        self.MQTT_BROKER_PORT = MQTT_BROKER_PORT
        self.MQTT_TOPIC_SUB = MQTT_TOPIC_SUB
        self.MQTT_TOPIC_PUB = MQTT_TOPIC_PUB






    def set_speed(self, speed):
        # Set the speed of the vehicle
        self.speed = speed

    def set_distance(self, distance):
        # Set the distance of the vehicle
        self.distance = distance

    @staticmethod

