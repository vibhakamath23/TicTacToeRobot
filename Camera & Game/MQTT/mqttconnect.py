# mqttconnect.py (for use on a desktop/macOS)

import paho.mqtt.client as mqtt

# MQTT Parameters
MQTT_SERVER = "10.247.137.92"
MQTT_PORT = 1883
MQTT_USER = ""  # Add if needed
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "XRP-Kamath"

# Called when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with code:", rc)

# Connect and return the client
def connect_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, MQTT_CLIENT_ID)
    client.on_connect = on_connect

    if MQTT_USER:
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

    try:
        client.connect(MQTT_SERVER, MQTT_PORT, 60)
        client.loop_start()  # Background thread
        return client
    except Exception as e:
        print("Error connecting to MQTT:", e)
        return None
