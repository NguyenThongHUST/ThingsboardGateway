
import random
from time import sleep
import time
from SX127x.LoRa import *
from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD
from paho.mqtt import client as mqtt_client
import json

broker = '127.0.0.1'
port = 1883
topic = "/sensor/data"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

BOARD.setup()

parser = LoRaArgumentParser("Continous LoRa receiver.")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

# client = mqtt_client.Client(client_id)
client = mqtt_client.Client()
client.on_connect = on_connect
client.connect(broker, port)

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
        self.set_freq(500)
        self.set_dio_mapping([0] * 6)
        self.set_rx_crc(True)

    def on_rx_done(self):
        BOARD.led_on()
        print("\nRxDone")
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        packet = json.loads(bytes(payload).decode("utf-8",'ignore'))
        # print("Sequence = " + str(packet['sequence']) + " deviceID = " + str(packet['deviceID']) + " Value = "+ str(packet['value']))
        x = {
            "serialNumber" : f"SN-{packet['deviceID']}",
            "sensorType" : "default",
            "sensorModel" : "T1000",
            "temp" : packet['temp'],
            "hum" : packet['hum'],
            "light" : packet['light'],
            "soil" : packet['soil'],
            "CO2" : 0,
            "sequence" : packet['sequence']
        }
        msg = json.dumps(x)
        publish(client, msg)
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        BOARD.led_off()
        self.set_mode(MODE.RXCONT)

    def on_tx_done(self):
        print("\nTxDone")
        print(self.get_irq_flags())

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
        while True:
            # sleep(.5)
            rssi_value = self.get_rssi_value()
            status = self.get_modem_status()
            sys.stdout.flush()
            sys.stdout.write("\r%d %d %d" % (rssi_value, status['rx_ongoing'], status['modem_clear']))
