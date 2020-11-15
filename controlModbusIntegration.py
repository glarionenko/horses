#!/usr/bin/env python3
import minimalmodbus
from time import *
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True
minimalmodbus.baudrate = 4800

# sleep(2)
instr2 = minimalmodbus.Instrument('COM9', 2)
instr2.serial.baudrate=4800
instr2.serial.timeout=5
instr2.serial.parity = minimalmodbus.serial.PARITY_NONE
instr2.serial.bytesize = 8
instr2.serial.stopbits = 2
instr2.debug=False

sleep(2)
counter=0
while True:
    try:
        counter=counter+1

        instr2.write_register(1,1,0)
        sleep(5)
        instr2.write_register(1,0,0)
        sleep(5)
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        print(e)
        pass
