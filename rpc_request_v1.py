
from threading import Thread
import threading
import random
import paho.mqtt.client as mqtt
import time
import json
from SX127x.LoRa import *
from SX127x.LoRa import LoRa2 as LoRa
from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD2 as BOARD
from paho.mqtt import client as mqtt_client
import RPi.GPIO as GPIO
from multiprocessing import Process, current_process
import threading

BOARD.setup()

parser = LoRaArgumentParser("Continous LoRa receiver.")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
    else:
        print(f"Connected fail with code {rc}")
    client.subscribe(topic='v1/devices/me/rpc/request/+', qos=2)
    # client.subscribe(topic='actuator/tester', qos=2)

def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    # client.publish(topic='v1/devices/me/attributes', payload = "ON:1")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("gOYfcBQuAONqR5nmHpBB")

client.connect("18.142.122.22", 1883, keepalive=60)
# client.connect("127.0.0.1", 1883, keepalive=60)
# client.loop_start()

try:
    client.loop_forever()
except KeyboardInterrupt:
    GPIO.cleanup()
