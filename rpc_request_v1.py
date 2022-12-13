
import random
import paho.mqtt.client as mqtt
import time
import json
from paho.mqtt import client as mqtt_client
import RPi.GPIO as GPIO
from multiprocessing import Process, current_process
import threading


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
    else:
        print(f"Connected fail with code {rc}")
    client.subscribe(topic='v1/devices/me/rpc/request/+', qos=1)

def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("Na5tkJmV9FRIUyhnqUEq")

client.connect("hustiot.tech", 1883, keepalive=60) # connect sensor to gateway


try:
    client.loop_forever()
except KeyboardInterrupt:
    GPIO.cleanup()
