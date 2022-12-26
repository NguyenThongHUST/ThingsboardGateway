
import random
from time import sleep
import time
from SX127x.LoRa import *
# from SX127x.LoRa import LoRa2 as LoRa
from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD as BOARD
from paho.mqtt import client as mqtt_client
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad
from sys import getsizeof
import base64
import json

key = b'aaaaaaaaaaaaaaaa' #global
iv = b'aaaaaaaaaaaaaaaa' #global




parser = LoRaArgumentParser("Continous LoRa receiver.")


def decrypt_aes(encrypted_message):
	try:
		cipher = AES.new(key, AES.MODE_CBC, iv)
		decrypted_msg = cipher.decrypt(encrypted_message);
		return decrypted_msg.decode("utf-8")
	except (ValueError, KeyError):
		print("Incorrect decryption")



def publish(client, msg):
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
        self.set_freq(501)
        self.set_dio_mapping([0] * 6)
        self.set_rx_crc(True)

    def on_rx_done(self):
        print("\nRxDone")
        print(self.get_irq_flags())
        print(map(hex, self.read_payload(nocheck=True)))
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)

    def on_tx_done(self):
        print("\nTx Done")
        global args
        self.set_mode(MODE.STDBY)
        self.clear_irq_flags(TxDone=1)
        sys.stdout.flush()
        self.tx_counter += 1
        sys.stdout.write("\rtx #%d" % self.tx_counter)
        self.set_mode(MODE.TX)

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
        self.set_freq(510)
        self.set_mode(MODE.STDBY)
        print(self.get_freq())
        # while True:
        # while True:
        #     sleep(1)   
            # sleep(.5)
            # rssi_value = self.get_rssi_value()
            # status = self.get_modem_status()
            # sys.stdout.flush()
            # sys.stdout.write("\r%d %d %d" % (rssi_value, status['rx_ongoing'], status['modem_clear']))
