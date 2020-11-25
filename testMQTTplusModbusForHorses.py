#!/usr/bin/env python3
import paho.mqtt.client as paho
import minimalmodbus
from time import *
import sys
import serial
import serial.tools.list_ports
from gpiozero import Button

button = Button(2, True)
#
ports = serial.tools.list_ports.comports() #automatic searching of ports
portArd = '1411' #change it for your arduino

for port1, desc, hwid in sorted(ports):
    print(hwid)
    if (hwid.find(portArd) != -1):
        print ("Arduino found")
        print (port1)
        arduino_port = port1
#arduino_port contains port

#add find arduino port here
#buy and prepeare bolid firmware to work with raspberry

#mqtt auth
#broker="188.242.123.156"
broker="192.168.50.127"
port=9001

#modbus start
#modbus start

instr1 = minimalmodbus.Instrument(arduino_port, 1)
instr1.serial.baudrate=4800
instr1.serial.timeout=5
instr1.serial.parity = minimalmodbus.serial.PARITY_NONE
instr1.serial.bytesize = 8
instr1.serial.stopbits = 2
instr1.debug=False
sleep(2)
print(instr1)
#
instr2 = minimalmodbus.Instrument(arduino_port, 2)
instr2.serial.baudrate=4800
instr2.serial.timeout=5
instr2.serial.parity = minimalmodbus.serial.PARITY_NONE
instr2.serial.bytesize = 8
instr2.serial.stopbits = 2
instr2.debug=False
sleep(2)
print(instr2)
#
instr3 = minimalmodbus.Instrument(arduino_port, 3)
instr3.serial.baudrate=4800
instr3.serial.timeout=5
instr3.serial.parity = minimalmodbus.serial.PARITY_NONE
instr3.serial.bytesize = 8
instr3.serial.stopbits = 2
instr3.debug=False
sleep(2)
print(instr3)
#
instr4 = minimalmodbus.Instrument(arduino_port, 4)
instr4.serial.baudrate=4800
instr4.serial.timeout=5
instr4.serial.parity = minimalmodbus.serial.PARITY_NONE
instr4.serial.bytesize = 8
instr4.serial.stopbits = 2
instr4.debug=False
sleep(2)
print(instr4)
#
instr5 = minimalmodbus.Instrument(arduino_port, 5)
instr5.serial.baudrate=4800
instr5.serial.timeout=5
instr5.serial.parity = minimalmodbus.serial.PARITY_NONE
instr5.serial.bytesize = 8
instr5.serial.stopbits = 2
instr5.debug=False
sleep(2)
#print(instr5)

sleep(2)
#
def on_connect(mqttc, obj, flags, rc):
    print("rc: "+str(rc))
    client1.subscribe("food/1")
    client1.subscribe("food/2")
    client1.subscribe("food/3")
    client1.subscribe("food/4")
    client1.subscribe("food/5")
    client1.subscribe("food/reset")
    client1.publish("test/check","off")
def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass
def on_message(client, userdata, message):
    global changed
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    #3 down 2 - up 1 stop
    if(message.topic=="food/1"):
        move_me(instr1,int(str(message.payload.decode("utf-8"))))
        #upd_me(instr1,"food/return/1")
    if(message.topic=="food/2"):
        move_me(instr2,int(str(message.payload.decode("utf-8"))))
    if(message.topic=="food/3"):
        move_me(instr3,int(str(message.payload.decode("utf-8"))))
    if(message.topic=="food/4"):
        move_me(instr4,int(str(message.payload.decode("utf-8"))))
    if(message.topic=="food/5"):
        move_me(instr5,int(str(message.payload.decode("utf-8"))))
    if(message.topic=="food/reset"):
        move_me(instr1,int(str(message.payload.decode("utf-8"))))
        sleep(20)
        move_me(instr2,int(str(message.payload.decode("utf-8"))))
        sleep(20)
        move_me(instr3,int(str(message.payload.decode("utf-8"))))
        sleep(20)
        move_me(instr4,int(str(message.payload.decode("utf-8"))))
        sleep(20)
        move_me(instr5,int(str(message.payload.decode("utf-8"))))
        sleep(20)
    #client.publish(id_to_topic_states[topic_to_id[message.topic]],str(changed[topic_to_id[message.topic]]))
    
client1= paho.Client("Horse1234",transport="websockets")                           #create client object
#client1._transport("websocket")
client1.username_pw_set("horse","55566678")
client1.on_publish = on_publish                          #assign function to callback
client1.on_message=on_message
client1.on_connect=on_connect
client1.connect(broker,port)
client1.loop_start()


bol=1
x=0
while True:
    try:
        x=x+1
        break # quit the loop if successful
    except:
        # error 
        pass
print(x)
""" def upd_me(instr, topic):
    started=time()
    done = 0
    while (time()-started<10.0) and (done<1):
        try:
            g=instr.read_register(2,0)
            client1.publish(topic,str(g))
            print(g)
            done = 1
            break
        except KeyboardInterrupt:
            sys.exit()
        except Exception as e:
            print(e)
            #continue
        if(done==1):
            break """
def move_me(instr,dir):
    started=time()
    done = 0
    while (time()-started<10.0) and (done<1):
        try:
            instr.write_register(1,dir,0)
            done = 1
            break
        except KeyboardInterrupt:
            sys.exit()
        except Exception as e:
            print(e)
            #continue
        if(done==1):
            break

while True:
    sleep(0.2)     