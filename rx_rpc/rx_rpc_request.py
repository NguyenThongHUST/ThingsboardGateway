
from multiprocessing import Process
import threading
import random
import paho.mqtt.client as mqtt
import time
import json
from paho.mqtt import client as mqtt_client
import RPi.GPIO as GPIO

TOKEN_MAP = {
    "SN-001": "Na5tkJmV9FRIUyhnqUEq",
    "SN-003": "soIsnoRIT6n7jsiN3J0B"
}

TIME_SCHEDULE = {
    "SN-001":0,
    "SN-003":0
}

THRESHOLD = 10

DURATION = {
    "SN-001":5,
    "SN-003":5
}

ledPin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.output(ledPin, False)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
    else:
        print(f"Connected fail with code {rc}")
    client.subscribe(topic='v1/devices/me/rpc/request/+', qos=1)

def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    json_object = json.loads(msg.payload.decode())
    date_time = int(json_object['params']['date']/1000)
    print(client._client_id.decode())
    TIME_SCHEDULE[client._client_id.decode()] = date_time
    print(type(client._client_id.decode()))

def schedule_action(date_time):
    print(int(time.time()))

def connect_mqtt(device_name):
    client = mqtt.Client(client_id = device_name)
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(TOKEN_MAP[device_name]) 

    client.connect("hustiot.tech", 1883, keepalive=60) # connect sensor to gateway
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        GPIO.cleanup()

class RxScheduleMsg(threading.Thread):
    def __init__(self, device_name):
        threading.Thread.__init__(self)
        self.device_name = device_name

    def run(self):
        print('Starting thread %s.' % self.device_name)
        connect_mqtt(self.device_name)
        print('Finished thread %s.' % self.device_name)

class HandleSchdule(threading.Thread):
    def __init__(self, device_name):
        threading.Thread.__init__(self)
        self.device_name = device_name

    def run(self):
        while True:
            # print(TIME_SCHEDULE[self.device_name])
            cur_time = time.time()
            threshold = DURATION[self.device_name]
            print(threshold)
            if((cur_time - threshold)< TIME_SCHEDULE[self.device_name] < (cur_time + threshold)):
                print(TIME_SCHEDULE[self.device_name])
                GPIO.output(ledPin, True)
                print(f"Do action for `{self.device_name}`")
            time.sleep(1)

def f1():
    thread1 = RxScheduleMsg("SN-001")
    thread2 = RxScheduleMsg("SN-003")
    thread3 = HandleSchdule("SN-001")
    thread4 = HandleSchdule("SN-003")

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()

    print('Finished.')  

if __name__ == '__main__':
    p1 = Process(name='Worker 1', target=f1)
    p1.start()
    p1.join()