
from threading import Thread
import threading
import re
from multiprocessing import Process
import time
import json
from time import sleep
from SX127x.LoRa import *
# from SX127x.LoRa import LoRa as LoRa
from SX127x.LoRaArgumentParser import LoRaArgumentParser
from paho.mqtt import client as mqtt_client
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad
from sys import getsizeof
import base64
import RPi.GPIO as GPIO
from SX127x.board_config import BOARD as BOARD

from LoRaRcvContClone import LoRaRcvCont

BOARD.setup()

broker = '18.142.122.22'
port = 1883
topic = "v1/devices/me/rpc/request/+"

key = b'aaaaaaaaaaaaaaaa' #global
iv = b'aaaaaaaaaaaaaaaa' #global

sequence = 1;

def encrypt_aes(decrypted_message):
	try:
		cipher = AES.new(key, AES.MODE_CBC, iv)
		msg = pad(decrypted_message.encode("utf-8"), AES.block_size)
		cipher_text = cipher.encrypt(msg);
		return base64.b64encode(cipher_text).decode('utf-8')
	except (ValueError, KeyError):
		print("Incorrect encryption")

def decrypt_aes(encrypted_message):
	try:
		cipher = AES.new(key, AES.MODE_CBC, iv)
		decode_msg = base64.b64decode(encrypted_message)
		decrypted_msg = cipher.decrypt(decode_msg);
		return decrypted_msg.decode("utf-8")
	except (ValueError, KeyError):
		print("Incorrect decryption")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)
    client.subscribe(topic='v1/devices/me/rpc/request/+', qos=2)

def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    payload = json.loads(msg.payload.decode());
    device_id = int(re.search(r'\d+', payload["params"]["name"])[0]);
    print(device_id);
    
    payload_t = {
        "type": 2,
        "seq": sequence,
        f'{payload["params"]["pin"]}': 1 if payload["params"]["value"] else 0
    }

    msg_payload_t = json.dumps(payload_t);

    msg_encrypted = encrypt_aes(msg_payload_t)
    print(encrypt_aes(msg_payload_t))

    packet_send = {
        "nt_id" : 1,
        "dv_id" : device_id,
        "gw_id" : 1,
        "ack" : 1,
        "payload" : msg_encrypted
    }
    packet_msg = json.dumps(packet_send);
    print(packet_msg);
    lora.write_payload(list(bytes(packet_msg, 'utf-8')));
    lora.set_mode(MODE.TX)

client = mqtt_client.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("gOYfcBQuAONqR5nmHpBB")

client.connect(broker, port)

parser = LoRaArgumentParser("Continous LoRa receiver.")

lora = LoRaRcvCont(verbose=False)
args = parser.parse_args(lora)

lora.set_mode(MODE.STDBY)
lora.set_pa_config(pa_select=1)

# print(lora)
assert(lora.get_agc_auto_on() == 1)
print("Here")

lora.start()

def rx_cont():
    # try: input("Press enter to start...")
    # except: pass

    try:
        # lora.start()
        client.loop_forever()
        GPIO.cleanup()
    except KeyboardInterrupt:
        sys.stdout.flush()
        print("")
        sys.stderr.write("KeyboardInterrupt\n")
    finally:
        sys.stdout.flush()
        print("")
        lora.set_mode(MODE.SLEEP)
        print(lora)
        BOARD.teardown()


if __name__ == '__main__':
    process1 = Process(target=rx_cont, args=())
    process1.start()
    print("Process1 Id: %i" %process1.pid)
    process1.join()

    print('Done.')