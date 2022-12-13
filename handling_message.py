
import random
import paho.mqtt.client as mqtt
import time
import json
from paho.mqtt import client as mqtt_client


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
    else:
        print(f"Connected fail with code {rc}")
    

def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")


client = mqtt.Client()
client.connect("127.0.0.1", 1883, keepalive=60) # connect sensor to gateway
client.on_connect = on_connect
client.on_message = on_message

msg = {
    "serialNumber": "SN-002",
    "sensorType": "Thermometer",
    "sensorModel": "T1000",
    "temp": 42,
    "hum": 50
}

msg = json.dumps(msg)
# print(msg)

for i in range(10):
  client.publish(topic='/sensor/data', payload=msg, qos=1)
  time.sleep(1)

client.loop_forever()
