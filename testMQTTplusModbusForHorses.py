#!/usr/bin/env python3
import paho.mqtt.client as paho
import minimalmodbus
from time import *
import sys
import serial
import serial.tools.list_ports
from gpiozero import Button

button = Button(2, True)
button_counter=0
button_long_hold_time=3
button_decision_time=2
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
#button_counter=0
#button_long_hold_time=3
#button_decision_time=2
was_pressed=0
decision_made=1
while True:
    if button.is_pressed:
        if(was_pressed==0):
            was_pressed=1
            started_at=time()  
    else:
        print("Released")
        if(was_pressed==1):
            button_counter=button_counter+1
            decison_made=0
            count_decision=time()
            how_long=time()-started_at
            was_pressed=0
        else:
            if(decision_made==0):
                if(time()-count_decision>button_decision_time):
                    if(button_counter>0):
                        if(how_long>button_long_hold_time):
                            #drop down or up all
                            print("full")
                            pass
                        else:
                            print("counter")
                            print(button_counter)
                            #counter switch
                            pass
                    button_counter=0
                    decision_made=1
    sleep(0.2)     