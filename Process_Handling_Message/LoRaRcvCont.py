
import random
from time import sleep
import time
from SX127x.LoRa import *
from SX127x.LoRa import LoRa2 as LoRa
from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD2 as BOARD
from paho.mqtt import client as mqtt_client
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad
from sys import getsizeof
import base64
import json

broker = '127.0.0.1'
port = 1883
topic = "/sensor/data"
ac_topc = "/actuator/data"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

key = b'aaaaaaaaaaaaaaaa' #global
iv = b'aaaaaaaaaaaaaaaa' #global

BOARD.setup()

parser = LoRaArgumentParser("Continous LoRa receiver.")


def decrypt_aes(encrypted_message):
	try:
		cipher = AES.new(key, AES.MODE_CBC, iv)
		decode_msg = base64.b64decode(encrypted_message)
		decrypted_msg = cipher.decrypt(decode_msg);
		return decrypted_msg.decode('utf-8').rstrip('\x00')
	except (ValueError, KeyError):
		print("Incorrect decryption")

def encrypt_aes(decrypted_message):
	try:
		cipher = AES.new(key, AES.MODE_CBC, iv)
		msg = pad(decrypted_message.encode("utf-8"), AES.block_size)
		cipher_text = cipher.encrypt(msg);
		return base64.b64encode(cipher_text).decode('utf-8')
	except (ValueError, KeyError):
		print("Incorrect encryption")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)
    client.subscribe(topic='v1/devices/me/rpc/request/+', qos=2)

def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
# client = mqtt_client.Client(client_id)
client = mqtt_client.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port)



def publish(client, msg, topic):
    if client.is_connected() == False :
        client.reconnect()
    result = client.publish(topic = topic, qos = 1, payload = msg)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic} {msg}")

class LoRaRcvCont(LoRa):
    def __init__(self, verbose=False):
        super(LoRaRcvCont, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        # self.set_freq(500)
        self.set_dio_mapping([0] * 6)
        self.set_rx_crc(True)

    def on_rx_done(self):
        BOARD.led_on()
        print("\nRxDone")
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        packet = json.loads(bytes(payload).decode("utf-8",'ignore'))

        print("\n Received msg: ")
        # print(bytes(payload).decode("utf-8",'ignore'))
        print(packet)

        decrypted_msg = decrypt_aes(packet["payload"]);
        

        print(decrypted_msg)

        payload_msg = json.loads(decrypted_msg);

        print(payload_msg)

        x = {
            "serialNumber" : f'SN-{packet["dv_id"]}',
        }

        for i in range(0,5):
            if f'{i}' in payload_msg:
                x[f'{i}'] = True if payload_msg[f'{i}'] == 1 else False
        
        msg = json.dumps(x)
        publish(client, msg, ac_topc)

        
        
        # msg_cipher = base64.b64decode(packet['payload']);

        # # print(msg_cipher)
        # print("\nDecrypted payload: ");
        # print(decrypt_aes(msg_cipher));


        # decrypt_msg = decrypt_aes(test_1)
        # print("The message was: ", decrypt_msg)
        # print(getsizeof(decrypt_msg))



        # data_test = json.loads(decrypt_msg)
        # print(data_test)
        # x = {
        #     "serialNumber" : f"SN-{packet['deviceID']}",
        #     "sensorType" : "default",
        #     "sensorModel" : "T1000",
        #     "temp" : packet['temp'],
        #     "hum" : packet['hum'],
        #     "light" : packet['light'],
        #     "soil" : packet['soil'],
        #     "CO2" : 0,
        #     "sequence" : packet['sequence']
        # }
        # msg = json.dumps(x)
        # publish(client, msg)
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        BOARD.led_off()
        self.set_mode(MODE.RXCONT)

    def on_tx_done(self):
        print("\nTxDone")
        self.set_mode(MODE.STDBY)
        self.clear_irq_flags(TxDone=1)

    def on_cad_done(self):
        print("\non_CadDone")
        print(self.get_irq_flags())

    def on_rx_timeout(self):
        print("\non_RxTimeout")
        print(self.get_irq_flags())

    def on_valid_header(self):
        print("\non_ValidHeader")
        print(self.get_irq_flags())

    def on_payload_crc_error(self):
        print("\non_PayloadCrcError")
        print(self.get_irq_flags())

    def on_fhss_change_channel(self):
        print("\non_FhssChangeChannel")
        print(self.get_irq_flags())

    def start(self):
        self.reset_ptr_rx()
        self.set_freq(500)
        self.set_mode(MODE.RXCONT)
        # while True:
        while True:
            sleep(1)   
            # sleep(.5)
            # rssi_value = self.get_rssi_value()
            # status = self.get_modem_status()
            # sys.stdout.flush()
            # sys.stdout.write("\r%d %d %d" % (rssi_value, status['rx_ongoing'], status['modem_clear']))
