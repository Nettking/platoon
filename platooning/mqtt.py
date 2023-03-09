import paho.mqtt.client as mqtt

# Define the MQTT broker address and port
MQTT_BROKER_ADDR = "localhost"
MQTT_BROKER_PORT = 1883

# Define the MQTT topics to subscribe and publish to
MQTT_TOPIC_SUB = "test/in"
MQTT_TOPIC_PUB = "test/out"

# Define the callback function for receiving MQTT messages
def on_message(client, userdata, message):
    # Decode the message payload from bytes to string
    payload = message.payload.decode()
    print("Received message: " + payload)

    # Publish a response message back to the specified topic
    client.publish(MQTT_TOPIC_PUB, "Received: " + payload)

# Set up the MQTT client and connect to the broker
client = mqtt.Client()
client.connect(MQTT_BROKER_ADDR, MQTT_BROKER_PORT)

# Set up the callback function for receiving messages
client.on_message = on_message

# Subscribe to the specified topic
client.subscribe(MQTT_TOPIC_SUB)

# Start the MQTT client loop to process incoming messages
client.loop_forever()
