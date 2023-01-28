from machine import Pin
import machine
import neopixel
from time import sleep


SLEEP_LENGTH = 0.25
GOOD_COLOR = (0,128,0)
MEDIUM_COLOR = (255,165,0)
BAD_COLOR = (255, 0, 0)
brightness=0.1

INFO_COLOR = (255,215,0)


def setup_led(pin):
    global np
    led_pin = Pin(pin)
    
    try:    
        np = neopixel.NeoPixel(pin=led_pin, n=1)
    except Exception as ex:
        print("error loading neopixel")
        print(ex)

    return np    

def on_good():
    on(GOOD_COLOR)
    
def on_water_soon():
    on(MEDIUM_COLOR)

def on_water_now():
    on(BAD_COLOR)

def blink_good():
    on_good()
    sleep(SLEEP_LENGTH)
    off()
    
def blink_water_soon():
    on_water_now()
    sleep(SLEEP_LENGTH)
    off()

def blink_water_now():
    on_water_now()
    sleep(SLEEP_LENGTH)
    off()

def blink_channel(channel_number):
    for _ in range(channel_number):
        on(INFO_COLOR)
        sleep(SLEEP_LENGTH)
        off()
        sleep(SLEEP_LENGTH)

def blink_error():
    for _ in range(4):
        on(BAD_COLOR)
        sleep(SLEEP_LENGTH)
        off()
        sleep(SLEEP_LENGTH)


def on(color):
    global np
    b_color = tuple([int(brightness*float(x)) for x in color])

    print(f"writing color {b_color}")
    np[0] = b_color
    np.write()
    
def off(pin_number = 0):
    global np
    if not np:
        np = setup_led(pin_number)
        
    np[0] = (0, 0, 0)
    np.write()
    
    
    
    
if __name__ == "__main__":
    try:

        setup_led(13)
        while True:
    
            blink_channel(8)
            # on(GOOD_COLOR)
            
            sleep(1)
            off()
            sleep(1)
            
    except KeyboardInterrupt:
        machine.reset()
