import paho.mqtt.client as mqtt
from pymongo import MongoClient
import json
import os
import logging

logging.basicConfig(level=logging.INFO)

# MongoDB setup
mongo_client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://mongodb:27017/'))
db = mongo_client[os.getenv('MONGODB_DATABASE', 'iot_database')]

# MQTT setup
mqtt_broker = os.getenv('MQTT_BROKER', 'mosquitto')
mqtt_port = int(os.getenv('MQTT_PORT', 1883))
mqtt_topic = os.getenv('MQTT_TOPIC', '/data')


# The callback for when the client receives a CONNACK response from the server.
def mqtt_on_connect(client, userdata, flags, reason_code, properties):
    global mqtt_topic
    
    logging.info(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(mqtt_topic)


# The callback for when a PUBLISH message is received from the server.
def mqtt_on_message(client, userdata, msg):
    global mongo_client, db
    logging.info(msg.topic+" "+str(msg.payload))
    try:
        payload = json.loads(msg.payload.decode())
        device_name = payload.get('device')
        if device_name:
            collection = db[device_name]
            collection.insert_one(payload)
            print(f"Message saved to {device_name} collection")
        else:
            print("Device name not found in payload")
    except Exception as e:
        print(f"Error processing message: {e}")


def main():
    global mqtt_broker, mqtt_port, mqtt_topic

    # Print the environment variables
    logging.info(f"MQTT_BROKER: {mqtt_broker}")
    logging.info(f"MQTT_PORT: {mqtt_port}")
    logging.info(f"MQTT_TOPIC: {mqtt_topic}")
    logging.info(f"MONGODB_URI: {os.getenv('MONGODB_URI', 'mongodb://mongodb:27017/')}")
    logging.info(f"MONGODB_DATABASE: {os.getenv('MONGODB_DATABASE', 'iot_database')}")

    # Create an MQTT client instance
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    # Assign the callback functions
    mqtt_client.on_connect = mqtt_on_connect
    mqtt_client.on_message = mqtt_on_message

    # Connect to the MQTT broker
    mqtt_client.connect(mqtt_broker, mqtt_port, 60)
    logging.info(f"Connected to MQTT broker at {mqtt_broker}:{mqtt_port}")

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    mqtt_client.loop_forever()


if __name__ == "__main__":
    main()
