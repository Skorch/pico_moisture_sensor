import network
import socket
from time import sleep
# from picozero import pico_temp_sensor, pico_led
import machine
# import mip
import ujson


led = machine.Pin("LED", machine.Pin.OUT)
led.value(1)

def get_ssid():
    with open('secrets.json') as fp:
        secrets = ujson.loads(fp.read())    
        
    ssid = secrets["wifi"]["ssid"]
    pwd = secrets["wifi"]["password"]
    
    return ssid, pwd
    
def connect(ssid, password):
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        
        led.toggle()    
        print(f'Waiting for connection... {wlan.status()}')
        sleep(1)

    led.on()
    # ip = wlan.ifconfig()[0]
    # print(f'Connected on {ip}')
    return wlan

# wlan = connect()
# install()
# setup_mqtt()

# try:
#     ip = connect()
#     install()
#     setup_mqtt()



# except KeyboardInterrupt:
#     machine.reset()

if __name__ == "__main__":
    ssid, pwd = get_ssid()
    wifi = connect(ssid, pwd)
    print(f'Connected on {wifi.ifconfig()[0]}')
