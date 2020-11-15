#!/usr/bin/env python3
import minimalmodbus
from time import *
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True
minimalmodbus.baudrate = 4800
# instr = minimalmodbus.Instrument('COM9', 1)
# instr.serial.baudrate=4800
# instr.serial.parity = minimalmodbus.serial.PARITY_NONE
# instr.serial.timeout=5

# instr.serial.bytesize = 8

# instr.serial.stopbits = 2


# instr.debug=False
# sleep(2)
instr2 = minimalmodbus.Instrument('COM9', 2)
instr2.serial.baudrate=4800
instr2.serial.timeout=5
instr2.serial.parity = minimalmodbus.serial.PARITY_NONE
instr2.serial.bytesize = 8
instr2.serial.stopbits = 2
instr2.debug=False
sleep(2)
#
# instr3 = minimalmodbus.Instrument('COM9', 3)
# instr3.serial.baudrate=4800
# instr3.serial.parity = minimalmodbus.serial.PARITY_NONE
# instr3.serial.timeout=5

# instr3.serial.bytesize = 8

# instr3.serial.stopbits = 2
""" #
sleep(2)
instr4 = minimalmodbus.Instrument('COM9', 1)
instr4.serial.baudrate=4800
instr4.serial.parity = minimalmodbus.serial.PARITY_NONE
instr4.serial.timeout=5

instr4.serial.bytesize = 8

instr4.serial.stopbits = 2
#
sleep(2)
instr5 = minimalmodbus.Instrument('COM9', 5)
instr5.serial.baudrate=4800
instr5.serial.parity = minimalmodbus.serial.PARITY_NONE
instr5.serial.timeout=5

instr5.serial.bytesize = 8

instr5.serial.stopbits = 2 """
sleep(2)
counter=0
while True:
    try:
        counter=counter+1
        # print(counter)
        # #print(instr)
        # sleep(3)
        # print(instr.read_register(0,0))
        # sleep(0.1)
        # print(instr2.read_register(0,0))
        # sleep(0.1)
        # instr.write_register(1,1,0)
        # sleep(0.1)
        # instr2.write_register(1,1,0)
        # sleep(0.1)
        # print(instr.read_register(1,0))
        # instr.write_register(1,0,0)
        # sleep(0.1)
        # instr2.write_register(1,0,0)
        # sleep(0.1)
        # print(instr.read_register(1,0))
        # sleep(0.1)
        # instr.write_register(1,1,0)
        # sleep(0.1)
        # instr2.write_register(1,1,0)
        # sleep(0.1)
        # print(instr.read_register(1,0))
        # instr.write_register(1,1,0)
        # sleep(0.1)
        # instr2.write_register(1,1,0)
        # sleep(0.1)
        # instr3.write_register(1,1,0)
        # sleep(3)
        # # instr4.write_register(1,1,0)
        # # sleep(0.1)
        # # instr5.write_register(1,1,0)
        # # #
        # # sleep(5)
        # instr.write_register(1,0,0)
        # sleep(0.1)
        # instr2.write_register(1,0,0)
        # sleep(0.1)
        # instr3.write_register(1,0,0)
        # sleep(0.1)
        # # instr4.write_register(1,0,0)
        # # sleep(0.1)
        # # instr5.write_register(1,0,0)
        # for x in range(250,0):
        #     instr3.write_register(2,x,0)
        #     sleep(0.05)
        # sleep(2)
        # instr3.write_register(1,0,0)
        # sleep(5)
        # instr3.write_register(1,1,0)
        # sleep(2)
        # for x in range(100,250):
        #     instr3.write_register(2,x,0)
        #     sleep(0.1)
        # sleep(5)
        instr2.write_register(1,1,0)
        sleep(5)
        instr2.write_register(1,0,0)
        sleep(5)
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        print(e)
        pass
