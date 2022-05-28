#import required library
import time
import pyfirmata

comport=''

board=pyfirmata.Arduino(comport)

led_1=board.get_pin('d:8:o')
led_2=board.get_pin('d:9:o')
led_3=board.get_pin('d:10:o')
led_4=board.get_pin('d:11:o')
led_6=board.get_pin('d:13:o')

def Alarm():
    led_6.write(1)
    time.sleep(5)
    led_6.write(0)

def led(total):


    if total==0:
        led_1.write(1)
        led_2.write(1)
        led_3.write(1)
        led_4.write(1)

    elif total==1:
        led_1.write(0)
        led_2.write(1)
        led_3.write(1)
        led_4.write(1)

    elif total==2:
        led_1.write(1)
        led_2.write(0)
        led_3.write(1)
        led_4.write(1)

    elif total==3:
        led_1.write(1)
        led_2.write(1)
        led_3.write(0)
        led_4.write(1)

    if total==4:
        led_1.write(1)
        led_2.write(1)
        led_3.write(1)
        led_4.write(0)

    elif total==5:
        led_1.write(0)
        led_2.write(0)
        led_3.write(0)
        led_4.write(0)
        