
#from pygame import mixer # Load the required library
import time
#mixer.init()
#mixer.music.load('amb.mp3')
#mixer.music.play(-1,0.0)
#time.sleep(3)
err=1
while err==1:
#if(1==1):
    try:
        exec(open('/home/pi/Desktop/MODBUS_play_TWO_videos_by_gpio.py').read())
        print("Runned")
        err=0;
    except:
        print("Eroor in running")
        time.sleep(5)
        err=1
        pass
