#!/usr/bin/env python3
import paho.mqtt.client as paho
import minimalmodbus
from time import *

#mqtt auth
broker="188.242.123.156"
port=9001

#modbus start
instr2 = minimalmodbus.Instrument('COM9', 2)
instr2.serial.baudrate=4800
instr2.serial.timeout=5
instr2.serial.parity = minimalmodbus.serial.PARITY_NONE
instr2.serial.bytesize = 8
instr2.serial.stopbits = 2
instr2.debug=False

sleep(2)
print(instr2)
sleep(2)
#
def on_connect(mqttc, obj, flags, rc):
    print("rc: "+str(rc))
    client1.subscribe("testtopic/1")
    client1.publish("house/bulb1","off")
def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass
def on_message(client, userdata, message):
    global changed
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
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
""" while True:
    try:
        # try code
        break # quit the loop if successful
    except:
        # error handling """
while True:
    try:
        instr2.write_register(1,1,0)
        sleep(0.5)
        instr2.write_register(1,0,0)
        sleep(0.5)
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        print(e)
        continue
        pass

        