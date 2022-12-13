

import random
import paho.mqtt.client as mqtt
import time
import json
from paho.mqtt import client as mqtt_client
import RPi.GPIO as GPIO


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
    else:
        print(f"Connected fail with code {rc}")

def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("S3kk2y12hdC6bvfuvycj")

# client.connect("127.0.0.1", 1883, keepalive=60)  #connect sensor to gateway

client.connect("hustiot.tech", 1883, keepalive=60)


msg = {
    "serialNumber": "SN-003",
    "sensorType": "Thermometer",
    "sensorModel": "T1000",
    "temp": 60,
    "hum": random.randint(0,80),
    "soil": 20,
	"light": 30,
	"CO2": 40,
    "sequence": 13
}

msg = json.dumps(msg)
# print(msg)

msg1 = {
    "temperature":20
}
msg1 = json.dumps(msg1)

for i in range(5):
    print("Send data to gateway\n")
    res = client.publish(topic="v1/devices/me/telemetry", qos=1, payload=msg1)
    print(res)
    print("\n")
    time.sleep(2)
    
try:
    client.loop_forever()
except KeyboardInterrupt:
    GPIO.cleanup()
