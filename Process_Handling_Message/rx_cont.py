
from threading import Thread
import threading
from multiprocessing import Process
import time
from time import sleep
from SX127x.LoRa import *
from SX127x.LoRa import LoRa2 as LoRa
from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD2 as BOARD

from LoRaRcvCont import LoRaRcvCont

BOARD.setup()

parser = LoRaArgumentParser("Continous LoRa receiver.")

lora = LoRaRcvCont(verbose=False)
args = parser.parse_args(lora)

lora.set_mode(MODE.STDBY)
lora.set_pa_config(pa_select=1)

print(lora)
assert(lora.get_agc_auto_on() == 1)

def rx_cont():
    # try: input("Press enter to start...")
    # except: pass

    try:
        lora.start()
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