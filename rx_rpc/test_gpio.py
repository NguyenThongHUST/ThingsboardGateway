
from multiprocessing import Process
import threading
import random
import paho.mqtt.client as mqtt
import time
import json
from paho.mqtt import client as mqtt_client
import RPi.GPIO as GPIO

ledPin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)

for i in range(10):
    GPIO.output(ledPin, True)
    time.sleep(2)
    GPIO.output(ledPin, False)
    time.sleep(2)

GPIO.cleanup()
