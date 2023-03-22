import paho.mqtt.client as mqtt

def send_message(client, MQTT_TOPIC_SUB, message = "Hello, world!"):
    # Publish a message to the specified topic
    client.publish(MQTT_TOPIC_SUB, message)
    print("Published message: " + message)

# Define the callback function for receiving MQTT messages
def on_message(client, MQTT_TOPIC_PUB, message):
    # Decode the message payload from bytes to string
    payload = message.payload.decode()
    response = "Received: " + payload
    print(response)
    # Publish a response message back to the specified topic
    send_message(client, MQTT_TOPIC_PUB, message = response)
    

def establish_connection(MQTT_BROKER_ADDR, MQTT_BROKER_PORT,MQTT_TOPIC_SUB, MQTT_TOPIC_PUB, message = "Hello, world!"):
    # Set up the MQTT client and connect to the broker
    client = mqtt.Client()
    client.connect(MQTT_BROKER_ADDR, MQTT_BROKER_PORT)

    # Set up the callback function for receiving messages
    client.on_message = on_message(client, MQTT_TOPIC_PUB, message)
    # Subscribe to the specified topic
    client.subscribe(MQTT_TOPIC_SUB)
    
    send_message(client, MQTT_TOPIC_SUB, message = message)

    # Start the MQTT client loop to process incoming messages
    client.loop_start()


def connect_to_all_brokers():
    # Define the MQTT broker address and port
    MQTT_BROKER_PORT = 1883

    # Define the MQTT topics to subscribe and publish to
    MQTT_TOPIC_SUB = "test/in"
    MQTT_TOPIC_PUB = "test/out"
    common_ip = "158.39.162."
    unique_ip = ["127","157","181","193"]
    
    for ip in unique_ip:
        full_ip = common_ip + ip
        establish_connection(full_ip, MQTT_BROKER_PORT,MQTT_TOPIC_SUB, MQTT_TOPIC_PUB)


if __name__ == '__main__':
    connect_to_all_brokers()